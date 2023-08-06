from hashlib import md5

from ksfctl.parser.ksf_parser import *
from ksfctl.parser.ksf_yacc import generate


class CppGenerator:
    def __init__(self, ast, filename, dest, **kwargs):
        self.__dict__.update(kwargs)
        self.ast = ast
        file = Path(filename)
        real_name = file.name
        self.ast_in_file = ast.files[real_name]

        Path(dest).mkdir(parents=True, exist_ok=True)
        self.generated_file = (Path(dest) / (real_name[:-4] + '.h'))

        self.inc_ordered = [
            "<string>",
            "<vector>",
            "<set>",
            "<unordered_set>",
            "<map>",
            "<unordered_map>",
            "<kup/Ksf.h>",
            "<kup/KsfJson.h>",
            "<servant/Agent.h>",
            "<servant/Servant.h>",
            "<promise/promise.h>",
        ]
        self.inc_native = {
            "<string>": True,
            "<vector>": False,
            "<set>": False,
            "<unordered_set>": False,
            "<map>": False,
            "<unordered_map>": False,
            "<kup/Ksf.h>": False,
            "<kup/KsfJson.h>": False,
            "<servant/Agent.h>": False,
            "<servant/Servant.h>": False,
            "<promise/promise.h>": False,
        }
        self.inc_depends = []
        self.file_str = ''
        self.curr_tab = ''

    def __getattr__(self, name):
        if name.startswith('with_') and not hasattr(self, 'name'):
            return False
        return super().__getattr__(name)

    def add_include(self, header):
        if header in self.inc_native:
            self.inc_native[header] = True
        else:
            self.inc_depends.append(header)

    def parse_header(self):
        output = ""
        for header in self.inc_ordered:
            if self.inc_native[header]:
                output += "#include " + header + "\n"

        output += "\n"

        for header in self.inc_depends:
            output += "#include " + header + "\n"
        return output

    def inc_tab(self):
        self.curr_tab += '\t'

    def del_tab(self):
        self.curr_tab = self.curr_tab[:-1]

    @staticmethod
    def get_type_id(curr_module, value_type):
        return f"{curr_module if value_type['module'] is None else value_type['module']}.{value_type['name']}"

    def is_movable_type(self, module, value_type):
        """判断是否是可以进行std::move的类型"""
        if value_type['type'] == 'native':
            return value_type['name'] == 'string'
        elif value_type['type'] == 'class':

            if hasattr(value_type, 'module'):
                class_full_name = value_type['module'] + "." + value_type['name']
            else:
                class_full_name = module + "." +value_type['name']

            return class_full_name not in self.ast.enums
        elif value_type['type'] == 'vector':
            return True
        elif value_type['type'] == 'map':
            return True
        else:
            return False

    def parse_type(self, module, value_type):
        if value_type['type'] == 'native':
            if value_type['name'] == 'string':
                self.add_include(f"<string>")
                return 'std::string'
            elif value_type['name'] == 'int':
                if value_type['bit'] == 8:
                    return f'{"unsigned char" if value_type["unsigned"] else "char"}'
                return f'{"u" if value_type["unsigned"] else ""}int{value_type["bit"]}_t'
            elif value_type['name'] == 'float':
                return value_type['name']
            elif value_type['name'] == 'double':
                return value_type['name']
            elif value_type['name'] == 'bool':
                return value_type['name']
            else:
                raise SyntaxError(f"不支持解析的字段类型[{value_type}]")
        elif value_type['type'] == 'class':
            if hasattr(value_type, 'module') and module != value_type['module']:
                return value_type['module'] + "::" + value_type['name']
            else:
                return value_type['name']
        elif value_type['type'] == 'vector':
            if value_type['is_ordered'] and not value_type['is_hashed'] and not value_type['is_unique_member']:
                true_type = 'std::vector'
                self.add_include('<vector>')
            elif value_type['is_ordered'] and not value_type['is_hashed'] and value_type['is_unique_member']:
                true_type = 'std::set'
                self.add_include('<set>')
            elif not value_type['is_ordered'] and value_type['is_hashed'] and value_type['is_unique_member']:
                true_type = 'std::unordered_set'
                self.add_include('<unordered_set>')
            else:
                raise SyntaxError(f"不支持解析的字段类型[{value_type}]")

            return f"{true_type}<{self.parse_type(module, value_type['value_type'])}>"
        elif value_type['type'] == 'map':
            if not value_type['is_ordered'] and value_type['is_hashed'] and value_type['is_unique_member']:
                true_type = 'std::unordered_map'
                self.add_include('<unordered_map>')
            elif value_type['is_ordered'] and not value_type['is_hashed'] and value_type['is_unique_member']:
                true_type = 'std::map'
                self.add_include('<map>')
            else:
                raise SyntaxError(f"不支持解析的字段类型[{value_type}]")
            return f"{true_type}<{self.parse_type(module, value_type['key_type'])}, {self.parse_type(module, value_type['value_type'])}>"

    def parse_comment_above(self, comment, tab=None):
        if comment is None or comment == '':
            return ''

        if tab is None:
            tab = self.curr_tab

        comment_lines = comment.split('\n')
        if len(comment_lines) == 1:
            return f"{tab}//{comment}\n"
        else:
            import re
            matches = re.findall(r"\s+\*\s+(.*)\n", f"/*{comment}*/")
            comment_str = f'{tab}/**\n'

            # 将每行注释内容拼接为Python风格的注释
            for match in matches:
                comment_str += f"{tab} * {match}\n"
            comment_str += f'{tab} */\n'
            return comment_str

    def parse_comment_line(self, comment):
        if comment is None or comment == '':
            return ''

        comment_lines = comment.split('\n')
        if len(comment_lines) == 1:
            return f" //{comment}"
        else:
            raise SyntaxError("不支持的注释方式")

    def parse_value(self, value):
        return value['value'] if value['is_number'] else f'"{value["value"]}"'

    def parse_const(self, curr_module, ksf_const: KsfConst):
        if ksf_const.value_type['name'] == 'string':
            return f"{self.parse_comment_above(ksf_const.comment)}{self.curr_tab}constexpr const char *{ksf_const.name} = {self.parse_value(ksf_const.value)};\n\n"
        return f"{self.parse_comment_above(ksf_const.comment)}{self.curr_tab}constexpr {self.parse_type(curr_module, ksf_const.value_type)} {ksf_const.name} = {self.parse_value(ksf_const.value)};\n\n"

    def parse_enum_member(self, ksf_enum_member: KsfEnumMember):
        return f"{self.curr_tab}{ksf_enum_member.name} = {ksf_enum_member.value}"

    def parse_enum_to_str(self, ksf_enum_member: KsfEnumMember):
        return f"{self.curr_tab}    case {ksf_enum_member.name}: return \"{ksf_enum_member.name}\";"

    def parse_str_to_enum(self, ksf_enum_member: KsfEnumMember):
        return f"{self.curr_tab}if (s == \"{ksf_enum_member.name}\") {{ e = {ksf_enum_member.name}; return 0; }}"

    def parse_default_var(self, name, value_type, default):
        if default is None:
            if value_type['name'] == 'int':
                return f'''if ({name} == 0) '''
            elif value_type['name'] == 'float':
                return f'if (ksf::KS_Common::equal(0.0f, {name})) '
            elif value_type['name'] == 'double':
                return f'if (ksf::KS_Common::equal(0.0, {name})) '
            elif value_type['name'] == 'bool':
                return f'if ({name})'
            elif value_type['name'] == 'string':
                return f'if ({name}.empty())'
            else:
                return ''

        # 特殊处理一下bool型
        if default['is_bool']:
            return f'if ({"" if default["value"] else "!"}{name})'
        elif default['is_number']:
            if value_type['name'] == 'float':
                return f'if (ksf::KS_Common::equal({name}f, {default["value"]})) '
            elif value_type['name'] == 'double':
                return f'if (ksf::KS_Common::equal({name}, {default["value"]})) '
            return f'if ({name} == {default["value"]}) '
        elif default['is_enum']:
            return f'if ({name} == {default["value"]}) '
        else:
            return f'if ({name} == "{default["value"]}") '

    def parse_enum(self, curr_module, ksf_enum: KsfEnum):
        enum_str = f"{self.parse_comment_above(ksf_enum.comment)}{self.curr_tab}enum {ksf_enum.name} \n{{\n"
        self.inc_tab()
        enum_member_str_list = []
        enum_member_tostr = []
        enum_member_strto = []
        for m in ksf_enum.member:
            enum_member_str_list.append(self.parse_enum_member(m))
            enum_member_tostr.append(self.parse_enum_to_str(m))
            enum_member_strto.append(self.parse_str_to_enum(m))

        self.del_tab()

        enum_str += ',\n'.join(enum_member_str_list)

        enum_str += f"\n}};\n\n"

        etos_member = '\n'.join(enum_member_tostr)
        enum_str += f"""\
inline std::string etos(const {ksf_enum.name} &e) {{
    switch (e) {{
{etos_member}
        default: return "";
    }}
}}

"""

        stoe_member = '\n'.join(enum_member_strto)
        enum_str += f"""\
inline int stoe(const std::string &s, {ksf_enum.name} &e) {{
{stoe_member}
    return -1;
}}

"""
        return enum_str

    def parse_variable(self, curr_module, ksf_var: KsfField):
        def parse_default_var(value_type, default):
            if default is None:
                if value_type['name'] == 'int':
                    return '0'
                elif value_type['name'] == 'float':
                    return '0.0f'
                elif value_type['name'] == 'double':
                    return '0.0'
                elif value_type['name'] == 'bool':
                    return 'true'
                elif value_type['name'] == 'string':
                    return '""'
                else:
                    return None

            # 特殊处理一下bool型
            if default['is_bool']:
                return f'{"true" if default["value"] else "false"}'
            elif default['is_number'] or default['is_enum']:
                return f'{default["value"]}'
            else:
                return f'"{default["value"]}"'
        default_var = parse_default_var(ksf_var.value_type, ksf_var.default)
        return f"{self.parse_type(curr_module, ksf_var.value_type)} \n{ksf_var.name}" \
               f"{' = ' + default_var if default_var is not None else ''}; " \
               f"{self.parse_comment_line(ksf_var.comment)}\n\n"
        pass

    def add_lines(self, lines, tab=None):
        if tab is None:
            tab = self.curr_tab

        return f"\n".join(tab + line for line in lines.split("\n")[:-1]) + '\n'

    def parse_resetDefault(self, curr_module, ksf_struct: KsfStruct):
        return self.add_lines(f'''\
/**
 * 重新赋值为初始构造的结构
 */
void resetDefault() {{
    *this = {ksf_struct.name}{{}}; 
}}\n''')

    def parse_variable_writeTo(self, ksf_field: KsfField):
        value_type = ksf_field.value_type
        if self.with_check_default:
            if value_type['type'] == 'native':
                if value_type['name'] != 'bool':
                    return f"""{self.parse_default_var(ksf_field.name, value_type, ksf_field.default)} {{_os.write({ksf_field.name}, {ksf_field.tag});}}"""
                else:
                    if ksf_field.default is None or ksf_field.default['value']:
                        return f"""if (!{ksf_field.name}) {{_os.write({ksf_field.name}, {ksf_field.tag});}}"""
                    else:
                        return f"""if ({ksf_field.name}) {{_os.write({ksf_field.name}, {ksf_field.tag});}}"""
            elif value_type['type'] == 'class':
                # 如果是枚举类型
                if value_type['name'] in self.ast.enums:
                    return f"_os.write((int32_t){ksf_field.name}, {ksf_field.tag});"
                else:
                    return f"_os.write({ksf_field.name}, {ksf_field.tag});"
            elif value_type['type'] == 'vector':
                return f"""if (!{ksf_field.name}.empty()) {{_os.write({ksf_field.name}, {ksf_field.tag});}}"""
            elif value_type['type'] == 'map':
                return f"""if (!{ksf_field.name}.empty()) {{_os.write({ksf_field.name}, {ksf_field.tag});}}"""
            else:
                raise SyntaxError(f"不能被解析的字段类型[{value_type}]")
        else:
            return f"_os.write({ksf_field.name}, {ksf_field.tag});"

    def parse_writeTo(self, curr_module, ksf_struct: KsfStruct):
        var_list = ""
        for var in ksf_struct.variable:
            var_list += self.parse_variable_writeTo(ksf_struct.variable[var]) + '\n'

        return self.add_lines(f'''\
/**
 * 序列化为二进制流
 */
template<typename WriterT>
void writeTo(ksf::KsfOutputStream<WriterT>& _os) const {{
{self.add_lines(var_list, '    ')}
}}\n''')

    def parse_variable_writeToJson(self, curr_module, ksf_field: KsfField):
        return f"""p->value["{ksf_field.name}"] = ksf::JsonOutput::writeJson({ksf_field.name});"""

    def parse_writeToJson(self, curr_module, ksf_struct: KsfStruct):
        var_list = ""
        for var in ksf_struct.variable:
            var_list += self.parse_variable_writeToJson(curr_module, ksf_struct.variable[var]) + '\n'

        return self.add_lines(f'''\
/**
 * 序列化为Json
 */
ksf::JsonValueObjPtr writeToJson() const {{
    ksf::JsonValueObjPtr p = new ksf::JsonValueObj();
{self.add_lines(var_list, '    ')}
    return p;
}}

/**
 * 序列化为Json字符串
 */
std::string writeToJsonString() const {{
    return ksf::KS_Json::writeValue(writeToJson());
}}\n''')

    def parse_variable_readFrom(self, curr_module, ksf_field: KsfField):
        value_type = ksf_field.value_type
        if value_type['type'] == 'native':
            return f"""_is.read({ksf_field.name}, {ksf_field.tag}, false);"""
        elif value_type['type'] == 'class':
            return f"""_is.read({ksf_field.name}, {ksf_field.tag}, false);"""
        elif value_type['type'] == 'vector':
            return f"""_is.read({ksf_field.name}, {ksf_field.tag}, false);"""
        elif value_type['type'] == 'map':
            return f"""_is.read({ksf_field.name}, {ksf_field.tag}, false);"""
        else:
            raise SyntaxError(f"不能被解析的字段类型[{value_type}]")

    def parse_readFrom(self, curr_module, ksf_struct: KsfStruct):
        var_list = ""
        for var in ksf_struct.variable:
            var_list += self.parse_variable_readFrom(curr_module, ksf_struct.variable[var]) + '\n'

        return self.add_lines(f'''\
/**
  * 二进制反序列化为结构体
  */
template<typename ReaderT>
void readFrom(ksf::KsfInputStream<ReaderT>& _is)
{{
    resetDefault();
{self.add_lines(var_list, '    ')}
}}\n''')

    def parse_variable_readFromJson(self, curr_module, ksf_field: KsfField):
        return f"""ksf::JsonInput::readJson({ksf_field.name}, pObj->value["{ksf_field.name}"], false);"""

    def parse_readFromJson(self, curr_module, ksf_struct: KsfStruct):
        var_list = ""
        for var in ksf_struct.variable:
            var_list += self.parse_variable_readFromJson(curr_module, ksf_struct.variable[var]) + '\n'

        return self.add_lines(f'''\
/**
 * Json反序列化为结构体
 */
void readFromJson(const ksf::JsonValuePtr &p, bool isRequire = true) {{
    resetDefault();
    if(NULL == p.get() || p->getType() != ksf::eJsonTypeObj)
    {{
        char s[128];
        snprintf(s, sizeof(s), "read 'struct' type mismatch, get type: %d.", (p.get() ? p->getType() : 0));
        throw ksf::KS_Json_Exception(s);
    }}

    ksf::JsonValueObjPtr pObj=ksf::JsonValueObjPtr::dynamicCast(p);
{self.add_lines(var_list, '    ')}
}}

/**
 * Json字符串反序列化为结构体
 */
void readFromJsonString(const std::string &str) {{
    readFromJson(ksf::KS_Json::getValue(str));
}}
\n''')

    def parse_display(self, curr_module, ksf_struct: KsfStruct):
        var_list = ""
        for var in ksf_struct.variable:
            field = ksf_struct.variable[var]
            if field.value_type['type'] == "class" and self.get_type_id(curr_module,
                                                                        field.value_type) in self.ast.enums:
                var_list += f'_ds.display(static_cast<int32_t>({ksf_struct.variable[var].name}),"{ksf_struct.variable[var].name}");\n'
            else:
                var_list += f'_ds.display({ksf_struct.variable[var].name},"{ksf_struct.variable[var].name}");\n'

        return self.add_lines(f'''\
/**
 * 打印
 */
std::ostream& display(std::ostream& _os, int _level=0) const
{{
    ksf::KsfDisplayer _ds(_os, _level);
{self.add_lines(var_list, '    ')}
    return _os;
}}\n''')

    def parse_displaySimple(self, curr_module, ksf_struct: KsfStruct):
        var_list = ""
        for var in ksf_struct.variable:
            field = ksf_struct.variable[var]
            if field.value_type['type'] == "class" and self.get_type_id(curr_module,
                                                                        field.value_type) in self.ast.enums:
                var_list += f'_ds.displaySimple(static_cast<int32_t>({ksf_struct.variable[var].name}), true);\n'
            else:
                var_list += f'_ds.displaySimple({ksf_struct.variable[var].name}, true);\n'

        return self.add_lines(f'''\
/**
 * 简单打印
 */
std::ostream& displaySimple(std::ostream& _os, int _level=0) const
{{
    ksf::KsfDisplayer _ds(_os, _level);
{self.add_lines(var_list, '    ')}
    return _os;
}}\n''')

    def parse_equal(self, curr_module, ksf_struct: KsfStruct):
        var_list = []
        for var in ksf_struct.variable:
            field = ksf_struct.variable[var]
            if field.value_type['type'] == "native" and field.value_type['name'] in {'float', 'double'}:
                var_list.append(f'ksf::KS_Common::equal(l.{field.name}, r.{field.name})')
            else:
                var_list.append(f'l.{field.name} == r.{field.name}')

        in_list = ' && '
        var_eq = in_list.join(var_list)
        return self.add_lines(f'''\
inline bool operator==(const {ksf_struct.name} &l, const {ksf_struct.name} &r) {{
    return {var_eq};
}}\n''')

    def parse_struct(self, curr_module, ksf_struct: KsfStruct):
        self.add_include("<kup/Ksf.h>")

        struct_str = f"{self.parse_comment_above(ksf_struct.comment)}"  # 注释(可能没有)

        # struct XXX : public ksf::KsfStructBase
        # {
        struct_str += self.add_lines(f"struct {ksf_struct.name} : public ksf::KsfStructBase\n{{\n")

        # public:
        struct_str += self.add_lines(f"public:\n")
        self.inc_tab()
        #     static std::string className()
        #     {
        #         return "xx.xxx";
        #     }
        #     static std::string MD5()
        #     {
        #         return "a123123123213";
        #     }
        struct_str += self.add_lines(f'''\
static std::string className() {{
    return "{ksf_struct.module}.{ksf_struct.name}";
}}

static std::string MD5() {{
    return "{md5(ksf_struct.id.encode('utf-8')).hexdigest()}";
}}\n''')
        self.del_tab()
        # public:
        struct_str += '\n'
        struct_str += self.add_lines(f"public:\n")

        self.inc_tab()
        # 解析字段
        #     std::string appname;
        #     std::string servername;
        #     std::string sFilename;
        #     std::string sFormat;
        #     std::string setdivision;
        #     ksf::Bool bHasSufix;
        #     ksf::Bool bHasAppNamePrefix;
        #     ksf::Bool bHasSquareBracket;
        #     std::string sConcatStr;
        #     std::string sSepar;
        #     std::string sLogType;
        for var in ksf_struct.variable:
            struct_str += self.add_lines(self.parse_variable(curr_module, ksf_struct.variable[var]))

        self.del_tab()
        # public:
        struct_str += '\n'
        struct_str += self.add_lines(f"public:\n")
        self.inc_tab()
        struct_str += self.parse_resetDefault(curr_module, ksf_struct)  # resetDefault

        struct_str += '\n'
        struct_str += self.parse_writeTo(curr_module, ksf_struct)  # writeTo

        struct_str += '\n'
        struct_str += self.parse_readFrom(curr_module, ksf_struct)  # readFrom

        if self.with_json:
            self.add_include("<kup/KsfJson.h>")
            struct_str += '\n'
            struct_str += self.parse_writeToJson(curr_module, ksf_struct)  # writeToJson

            struct_str += '\n'
            struct_str += self.parse_readFromJson(curr_module, ksf_struct)  # readFromJson

        struct_str += '\n'
        struct_str += self.parse_display(curr_module, ksf_struct)  # display

        struct_str += '\n'
        struct_str += self.parse_displaySimple(curr_module, ksf_struct)  # displaySimple

        self.del_tab()
        # };
        struct_str += f"{self.curr_tab}}};\n"

        # inline bool operator==(const {ksf_struct.name}&l, const {ksf_struct.name}&r)
        struct_str += '\n'
        # operator==
        struct_str += self.parse_equal(curr_module, ksf_struct)

        struct_str += '\n'
        # operator!=
        struct_str += f"""\
inline bool operator!=(const {ksf_struct.name} &l, const {ksf_struct.name} &r) {{
    return !(l == r);
}}\n"""
        if len(ksf_struct.key_fields) != 0:
            struct_str += f"""\
inline bool operator<(const {ksf_struct.name} &l, const {ksf_struct.name} &r) {{\n"""
            for key_field in ksf_struct.key_fields:
                struct_str += f"""\
    if(l.{key_field} != r.{key_field})  return (l.{key_field} < r.{key_field});\n"""
            struct_str += f"""\
    return false;
}}

inline bool operator<=(const {ksf_struct.name} &l, const {ksf_struct.name} &r) {{
    return !(r < l);
}}

inline bool operator>(const {ksf_struct.name} &l, const {ksf_struct.name} &r) {{
    return r < l;
}}

inline bool operator>=(const {ksf_struct.name} &l, const {ksf_struct.name} &r) {{
    return !(l < r);
}}\n\n"""

        if self.with_json:

            struct_str += '\n'
            # operator<<
            struct_str += f"""\
inline std::ostream &operator<<(std::ostream &os, const {ksf_struct.name} &r) {{
    os << r.writeToJsonString();
    return os;
}}"""

            struct_str += '\n'
            # operator>>
            struct_str += f"""\
inline std::istream &operator>>(std::istream &is, {ksf_struct.name} &l) {{
    std::istreambuf_iterator<char> eos;
    std::string s(std::istreambuf_iterator<char>(is), eos);
    l.readFromJsonString(s);
    return is;
}}\n"""
        return struct_str

    def parse_InterfacePrxCallBack(self, curr_module, ksf_interface: KsfInterface):
        prx_str = f"""\
class {ksf_interface.name}PrxCallback : public ksf::AgentCallback
{{
public:
    virtual ~{ksf_interface.name}PrxCallback() = default;
    
public:
\n"""

        index = 0
        func_case_str = ""
        for item in ksf_interface.operator:
            operator = ksf_interface.operator[item]

            def parse_output_vars(with_type=True):
                def parse_output_var(value_type, name, with_type):
                    if value_type['name'] != 'void':
                        if not self.is_movable_type(curr_module, value_type):
                            return f"{self.parse_type(curr_module, value_type)} {name}" if with_type else name
                        elif self.with_param_rvalue_ref:
                            return f"{self.parse_type(curr_module, value_type)} &&{name}" if with_type else f"std::move({name})"
                        else:
                            return f"const {self.parse_type(curr_module, value_type)} &{name}" if with_type else name
                vars_list = []
                if operator.return_type['name'] != 'void':
                    vars_list.append(parse_output_var(operator.return_type, '_ret', with_type))

                for i in operator.output:
                    vars_list.append(parse_output_var(operator.output[i].value_type, operator.output[i].name, with_type))

                return ', '.join(vars_list)

            prx_str += f"""\
    virtual void callback_{operator.name}({parse_output_vars(True)}) \
{{ throw std::runtime_error("callback_{operator.name} override incorrect."); }}
    
    virtual void callback_{operator.name}_exception(int32_t ret) \
{{ throw std::runtime_error("callback_{operator.name}_exception override incorrect."); }}
                
"""

            def parse_var_dispatch(var, name, index):
                if var['name'] == 'void':
                    return ""

                return f"""\
                {self.parse_type(curr_module, var)} {name};
                _is.read({name}, {index}, true);\n\n"""

            def parse_func_dispatch():
                """处理函数的分发"""
                func_case_str = f"""
            case {index}: {{
                if (msg->response->iRet != ksf::KSFSERVERSUCCESS) {{
                    callback_{operator.name}_exception(msg->response->iRet);
                    return msg->response->iRet;
                }}
                
                ksf::KsfInputStream<ksf::BufferReader> _is;
                
                _is.setBuffer(msg->response->sBuffer);\n\n"""

                func_case_str += parse_var_dispatch(operator.return_type, '_ret', 0)

                for i in operator.output:
                    var = operator.output[i]
                    func_case_str += parse_var_dispatch(var.value_type, var.name, var.index)

                func_case_str += f"""\
                
                ksf::CallbackThreadData *pCbtd = ksf::CallbackThreadData::getData();
                assert(pCbtd != NULL);
                
                pCbtd->setResponseContext(msg->response->context);
                
                callback_{operator.name}({parse_output_vars(False)});
                
                pCbtd->delResponseContext();
                
                return ksf::KSFSERVERSUCCESS;
            }}"""
                return func_case_str

            func_case_str += parse_func_dispatch()
            index += 1

        # 函数列表
        prx_str += f"""\
public:
    virtual const std::map<std::string, std::string> &getResponseContext() const {{
        ksf::CallbackThreadData *pCbtd = ksf::CallbackThreadData::getData();
        assert(pCbtd != NULL);
        
        if (!pCbtd->getContextValid()) {{
            throw ksf::KS_Exception("cann't get response context");
        }}
        return pCbtd->getResponseContext();
    }}\n\n"""

        prx_str += f"""\
public:
    int onDispatch(ksf::ReqMessagePtr msg) override
    {{
        static std::string __{ksf_interface.name}_all[] = {{"{'", "'.join(ksf_interface.operator.keys())}"}};
                                            
        std::pair<std::string *, std::string *> r = equal_range(__{ksf_interface.name}_all, __{ksf_interface.name}_all + 9, std::string(msg->request.sFuncName));
        
        if (r.first == r.second) {{
            return ksf::KSFSERVERNOFUNCERR;
        }}
        
        switch (r.first - __{ksf_interface.name}_all) {{
{func_case_str}
        }} //end switch
        
        return ksf::KSFSERVERNOFUNCERR;
    }} //end onDispatch\n"""

        prx_str += f"""}}; //end {ksf_interface.name}PrxCallback

using {ksf_interface.name}PrxCallbackPtr = ksf::KS_AutoPtr<{ksf_interface.name}PrxCallback>;\n\n"""

        return prx_str

    def parse_InterfacePrxCallbackPromise(self, curr_module, ksf_interface: KsfInterface):
        parsed_str = f"""\
class {ksf_interface.name}PrxCallbackPromise: public ksf::AgentCallback
{{
public:
    virtual ~{ksf_interface.name}PrxCallbackPromise() = default;
\n"""

        dispatch_case_str = ""
        case_index = 0
        for item in ksf_interface.operator:
            operator = ksf_interface.operator[item]
            parsed_str += f"""\
public:
    struct Promise{operator.name}: virtual public KS_HandleBase {{
    public:
        std::map<std::string, std::string> _mRspContext;\n"""

            if operator.return_type['name'] != 'void':
                parsed_str += f"        {self.parse_type(curr_module, operator.return_type)} _ret;\n"

            for item in operator.output:
                var = operator.output[item]
                parsed_str += f"        {self.parse_type(curr_module, var.value_type)} {var.name};\n"

            parsed_str += f"""\
    }};
        
    using Promise{operator.name}Ptr = ksf::KS_AutoPtr<{ksf_interface.name}PrxCallbackPromise::Promise{operator.name}>;
    
    {ksf_interface.name}PrxCallbackPromise(const ksf::Promise<{ksf_interface.name}PrxCallbackPromise::Promise{operator.name}Ptr> &promise)
    : _promise_{operator.name}(promise) {{}}
    
    virtual void callback_{operator.name}(const {ksf_interface.name}PrxCallbackPromise::Promise{operator.name}Ptr &ptr) {{
        _promise_{operator.name}.setValue(ptr);
    }}
    
    virtual void callback_{operator.name}_exception(ksf::Int32 ret) {{
        std::stringstream oss;
        oss << "Function:{operator.name}_exception|Ret:";
        oss << ret;
        _promise_{operator.name}.setException(ksf::copyException(oss.str(), ret));
    }}
    
protected:
    ksf::Promise<{ksf_interface.name}PrxCallbackPromise::Promise{operator.name}Ptr > _promise_{operator.name};\n\n"""

            def parse_var_dispatch(var, name, index):
                if var['name'] == 'void':
                    return ""

                return f"""\
                    _is.read(ptr->{name}, {index}, true);\n"""

            def parse_func_dispatch():
                """处理函数的分发"""
                func_case_str = f"""\
            case {case_index}: {{
                if (msg->response->iRet != ksf::KSFSERVERSUCCESS) {{
                    callback_{operator.name}_exception(msg->response->iRet);
                    return msg->response->iRet;
                }}

                ksf::KsfInputStream<ksf::BufferReader> _is;
                _is.setBuffer(msg->response->sBuffer);
                {ksf_interface.name}PrxCallbackPromise::Promise{operator.name}Ptr ptr = new {ksf_interface.name}PrxCallbackPromise::Promise{operator.name}();
                
                try {{\n"""

                func_case_list = []
                ret = parse_var_dispatch(operator.return_type, '_ret', 0)
                if ret != "":
                    func_case_list.append(ret)

                for item2 in operator.output:
                    var2 = operator.output[item2]
                    func_case_list.append(parse_var_dispatch(var2.value_type, var2.name, var2.index))

                func_case_str += ''.join(func_case_list)
                return func_case_str
            case_index += 1
            dispatch_case_str += parse_func_dispatch()
            dispatch_case_str += f"""\
                }} catch (std::exception &ex) {{
                    callback_{operator.name}_exception(ksf::KSFCLIENTDECODEERR);
                    return ksf::KSFCLIENTDECODEERR;
                }} catch (...) {{
                    callback_{operator.name}_exception(ksf::KSFCLIENTDECODEERR);
                    return ksf::KSFCLIENTDECODEERR;
                }}
                
                ptr->_mRspContext = msg->response->context;
                callback_{operator.name}(ptr);
                return ksf::KSFSERVERSUCCESS;
            }}\n"""

        parsed_str += f"""\
public:
    int onDispatch(ksf::ReqMessagePtr msg) override
    {{
        static std::string __{ksf_interface.name}_all[] = {{"{'", "'.join(ksf_interface.operator.keys())}"}};

        std::pair<std::string *, std::string *> r = equal_range(__{ksf_interface.name}_all, __{ksf_interface.name}_all + 9, std::string(msg->request.sFuncName));

        if (r.first == r.second) {{
            return ksf::KSFSERVERNOFUNCERR;
        }}

        switch (r.first - __{ksf_interface.name}_all) {{\n"""
        parsed_str += dispatch_case_str
        parsed_str += f"""\
        }} //end switch
        
        return ksf::KSFSERVERNOFUNCERR;
    }} //end onDispatch\n"""

        parsed_str += f"\n}}; //end {ksf_interface.name}PrxCallbackPromise\n\n" \
                      f"using {ksf_interface.name}PrxCallbackPromisePtr = ksf::KS_AutoPtr<{ksf_interface.name}PrxCallbackPromise>;\n" \
                      f"\n"
        return parsed_str

    def parse_InterfaceCoroPrxCallback(self, curr_module, ksf_interface: KsfInterface):
        def parse_var_dispatch(var, name, index):
            if var['name'] == 'void':
                return ""

            return f"""\
                    {self.parse_type(curr_module, var)} {name};
                    _is.read({name}, {index}, true);\n\n"""

        def parse_func_dispatch():
            """处理函数的分发"""
            func_case_str = ""
            index = 0
            for item in ksf_interface.operator:
                operator = ksf_interface.operator[item]

                def parse_output_vars(with_type=True):
                    def parse_output_var(value_type, name, with_type):
                        if value_type['name'] != 'void':
                            if not self.is_movable_type(curr_module, value_type):
                                return f"{self.parse_type(curr_module, value_type)} {name}" if with_type else name
                            elif self.with_param_rvalue_ref:
                                return f"{self.parse_type(curr_module, value_type)} &&{name}" if with_type else f"std::move({name})"
                            else:
                                return f"const {self.parse_type(curr_module, value_type)} &{name}" if with_type else name

                    vars_list = []
                    if operator.return_type['name'] != 'void':
                        vars_list.append(parse_output_var(operator.return_type, '_ret', with_type))

                    for item in operator.output:
                        vars_list.append(
                            parse_output_var(operator.output[item].value_type, operator.output[item].name, with_type))

                    return ', '.join(vars_list)

                func_case_str += f"""
            case {index}: {{
                if (msg->response->iRet != ksf::KSFSERVERSUCCESS) {{
                    callback_{operator.name}_exception(msg->response->iRet);
                    return msg->response->iRet;
                }}
    
                ksf::KsfInputStream<ksf::BufferReader> _is;
                _is.setBuffer(msg->response->sBuffer);
    
                try {{\n"""
                func_case_list = []
                ret = parse_var_dispatch(operator.return_type, '_ret', 0)
                if ret != "":
                    func_case_list.append(ret)

                for item2 in operator.output:
                    var2 = operator.output[item2]
                    func_case_list.append(parse_var_dispatch(var2.value_type, var2.name, var2.index))

                func_case_str += ''.join(func_case_list)

                func_case_str += f"""\
                    callback_{operator.name}({parse_output_vars(with_type=False)});
                }} catch (std::exception &ex) {{
                    callback_{operator.name}_exception(ksf::KSFCLIENTDECODEERR);
                    return ksf::KSFCLIENTDECODEERR;
                }} catch (...) {{
                    callback_{operator.name}_exception(ksf::KSFCLIENTDECODEERR);
                    return ksf::KSFCLIENTDECODEERR;
                }}
    
                return ksf::KSFSERVERSUCCESS;
            }}\n"""

                index += 1

            return func_case_str

        parsed_str = f"""\
class {ksf_interface.name}CoroPrxCallback : public {ksf_interface.name}PrxCallback
{{
public:
    virtual ~{ksf_interface.name}CoroPrxCallback() = default;

public:
    const std::map<std::string, std::string> &getResponseContext() const override {{ return _mRspContext; }}
    
    virtual void setResponseContext(const std::map<std::string, std::string> &mContext) {{ _mRspContext = mContext; }}
"""
        parsed_str += f"""\
public:
    int onDispatch(ksf::ReqMessagePtr msg) override
    {{
        static std::string __{ksf_interface.name}_all[] = {{"{'", "'.join(ksf_interface.operator.keys())}"}};

        std::pair<std::string *, std::string *> r = equal_range(__{ksf_interface.name}_all, __{ksf_interface.name}_all + 9, std::string(msg->request.sFuncName));

        if (r.first == r.second) {{
            return ksf::KSFSERVERNOFUNCERR;
        }}

        switch (r.first - __{ksf_interface.name}_all) {{
{parse_func_dispatch()}
        }} //end switch
        
        return ksf::KSFSERVERNOFUNCERR;
    }} //end onDispatch

protected:
    std::map<std::string, std::string> _mRspContext;
}}; //end {ksf_interface.name}CoroPrxCallback

typedef ksf::KS_AutoPtr<{ksf_interface.name}CoroPrxCallback> {ksf_interface.name}CoroPrxCallbackPtr;\n"""
        return parsed_str

    def parse_InterfaceProxy(self, curr_module, ksf_interface: KsfInterface):
        def parse_operators():
            parsed_oper_str = ""
            for item in ksf_interface.operator:
                operator = ksf_interface.operator[item]

                def has_return():
                    return operator.return_type['name'] != 'void'

                def parse_input_vars():
                    parsed_list = []
                    for name in operator.input:
                        var = operator.input[name]
                        parsed_list.append(f"""\
        _os.write({name}, {var.index});\n""")
                    return parsed_list

                def parse_output_vars():
                    parsed_list = []
                    if operator.return_type['name'] != 'void':
                        parsed_list.append(f"""\
        {self.parse_type(curr_module, operator.return_type)} _ret;
        _is.read(_ret, 0, true);\n""")

                    for name in operator.output:
                        var = operator.output[name]
                        parsed_list.append(f"""\
        _is.read({name}, {var.index}, true);\n""")
                    return parsed_list

                def parse_all_vars(with_output=False):
                    parsed_list = []
                    for var_name, is_output in operator.ordered_var:
                        if is_output:
                            if with_output:
                                parsed_list.append(
                                    f"{self.parse_type(curr_module, operator.output[var_name].value_type)} &{var_name}, ")
                        else:
                            parsed_list.append(
                                f"const {self.parse_type(curr_module, operator.input[var_name].value_type)} &{var_name}, ")

                    return parsed_list

                parsed_oper_str += f"""\
public:
{self.parse_comment_above(operator.comment, tab='    ')}\
    {self.parse_type(curr_module, operator.return_type) if has_return() else 'void'} {operator.name}({''.join(parse_all_vars(True))}const std::map<std::string, std::string> &mapReqContext = KSF_CONTEXT(), std::map<std::string, std::string> *pResponseContext = NULL) {{
        ksf::KsfOutputStream<ksf::BufferWriterVector> _os;
{''.join(parse_input_vars())}
        std::map<std::string, std::string>   _mStatus;
        std::shared_ptr<ksf::ResponsePacket> rep = ksf_invoke(ksf::KSFNORMAL, "{operator.name}", _os, mapReqContext, _mStatus);
        if (pResponseContext) {{
            pResponseContext->swap(rep->context);
        }}
        
        ksf::KsfInputStream<ksf::BufferReader> _is;
        _is.setBuffer(rep->sBuffer);
{''.join(parse_output_vars())}
        {'return _ret;' if has_return() else ''}
    }}
    
    void async_{operator.name}({ksf_interface.name}PrxCallbackPtr callback, {''.join(parse_all_vars())}const std::map<std::string, std::string> &context = KSF_CONTEXT()) {{
        ksf::KsfOutputStream<ksf::BufferWriterVector> _os;
{''.join(parse_input_vars())}
        std::map<std::string, std::string> _mStatus;
        ksf_invoke_async(ksf::KSFNORMAL, "{operator.name}", _os, context, _mStatus, callback);
    }}
    
    ksf::Future<{ksf_interface.name}PrxCallbackPromise::Promise{operator.name}Ptr> promise_async_{operator.name}({''.join(parse_all_vars())}const std::map<std::string, std::string> &context) {{
        ksf::Promise<{ksf_interface.name}PrxCallbackPromise::Promise{operator.name}Ptr> promise;
        {ksf_interface.name}PrxCallbackPromisePtr callback = new {ksf_interface.name}PrxCallbackPromise(promise);
        
        ksf::KsfOutputStream<ksf::BufferWriterVector> _os;
{''.join(parse_input_vars())}
        std::map<std::string, std::string> _mStatus;
        ksf_invoke_async(ksf::KSFNORMAL, "{operator.name}", _os, context, _mStatus, callback);
        
        return promise.getFuture();
    }}
    
    void coro_{operator.name}({ksf_interface.name}CoroPrxCallbackPtr callback, {''.join(parse_all_vars())}const std::map<std::string, std::string> &context = KSF_CONTEXT())
    {{
        ksf::KsfOutputStream<ksf::BufferWriterVector> _os;
{''.join(parse_input_vars())}
        std::map<std::string, std::string>            _mStatus;
        ksf_invoke_async(ksf::KSFNORMAL, "{operator.name}", _os, context, _mStatus, callback, true);
    }}\n\n"""
            return parsed_oper_str

        parsed_str = f"""\
class {ksf_interface.name}Proxy : public ksf::Agent
{{
public:
    typedef std::map<std::string, std::string> KSF_CONTEXT;
    
public:
    {ksf_interface.name}Proxy* ksf_hash(uint32_t key) {{
        return ({ksf_interface.name}Proxy*)Agent::ksf_hash(key);
    }}

    {ksf_interface.name}Proxy* ksf_consistent_hash(uint32_t key) {{
        return ({ksf_interface.name}Proxy*)Agent::ksf_consistent_hash(key);
    }}

    {ksf_interface.name}Proxy* ksf_open_trace(bool traceParam = false) {{
        return ({ksf_interface.name}Proxy*)Agent::ksf_open_trace(traceParam);
    }}

    {ksf_interface.name}Proxy* ksf_set_timeout(int msecond) {{
        return ({ksf_interface.name}Proxy*)Agent::ksf_set_timeout(msecond);
    }}

    static const char* ksf_prxname() {{ return "{ksf_interface.name}Proxy"; }}
    
{parse_operators()}
}}; //end {ksf_interface.name}Proxy

using {ksf_interface.name}Prx = ksf::KS_AutoPtr<{ksf_interface.name}Proxy>;\n\n"""

        return parsed_str

    def parse_InterfaceObj(self, curr_module, ksf_interface: KsfInterface):
        parsed_str = f"""\
class {ksf_interface.name} : public ksf::Servant
{{
public:
    ~{ksf_interface.name}() override = default;
    
public:
/*必须继承并实现的函数*/
"""
        parsed_async_str = ''
        parsed_push_str = ''
        dispatch_case_str = ""
        index = 0
        for item in ksf_interface.operator:
            operator = ksf_interface.operator[item]

            def has_return():
                return operator.return_type['name'] != 'void'

            def parse_invoke_vars():
                parsed_list = []
                for name, is_output in operator.ordered_var:
                    if not is_output:
                        var = operator.input[name]
                        if self.with_param_rvalue_ref and self.is_movable_type(curr_module, var.value_type):
                            parsed_list.append(f"""std::move({var.name}), """)
                        else:
                            parsed_list.append(f"""{var.name}, """)
                    else:
                        var = operator.output[name]
                        parsed_list.append(f"""{var.name}, """)

                return ''.join(parsed_list)

            def parse_vars_list(tab=None):
                parsed_list = []
                for name, is_output in operator.ordered_var:
                    if not is_output:
                        var = operator.input[name]
                    else:
                        var = operator.output[name]
                    parsed_list.append(f"""{self.parse_type(curr_module, var.value_type)} {var.name};""")

                return '\n'.join([' ' * (4 * tab) + line for line in parsed_list])

            def parse_output_vars(mode='ksf', tab=None):
                if tab is None:
                    tab = 0

                parsed_list = []
                if operator.return_type['name'] != 'void':
                    if mode == 'ksf':
                        parsed_list.append(f"""_os.write(_ret, 0);""")
                    elif mode == 'kup':
                        parsed_list.append(f"""_ksfAttr_.put("", _ret);""")
                        parsed_list.append(f"""_ksfAttr_.put("ksf_ret", _ret);""")
                    elif mode == 'json':
                        parsed_list.append(f"""_p->value["ksf_ret"] = ksf::JsonOutput::writeJson(_ret);""")

                for name in operator.output:
                    var = operator.output[name]
                    if mode == 'ksf':
                        parsed_list.append(f"""_os.write({name}, {var.index});""")
                    elif mode == 'kup':
                        parsed_list.append(f"""_ksfAttr_.put("{name}", {name});""")
                    elif mode == 'json':
                        parsed_list.append(f"""_p->value["{name}"] = ksf::JsonOutput::writeJson({name});""")
                return '\n'.join([' ' * (4 * tab) + line for line in parsed_list])

            def parse_all_vars(with_input=False):
                parsed_list = []
                if not with_input and has_return():
                    parsed_list.append(f", const {self.parse_type(curr_module, operator.return_type)} &_ret")

                for var_name, is_output in operator.ordered_var:
                    if is_output:
                        if with_input:
                            parsed_list.append(
                                f"{self.parse_type(curr_module, operator.output[var_name].value_type)} &{var_name}, ")
                        else:
                            parsed_list.append(
                                f", const {self.parse_type(curr_module, operator.output[var_name].value_type)} &{var_name}")
                    elif with_input:
                        if self.is_movable_type(curr_module, operator.input[var_name].value_type):
                            if self.with_param_rvalue_ref:
                                parsed_list.append(
                                    f"{self.parse_type(curr_module, operator.input[var_name].value_type)} &&{var_name}, ")
                            else:
                                parsed_list.append(
                                    f"const {self.parse_type(curr_module, operator.input[var_name].value_type)} &{var_name}, ")
                        else:
                            parsed_list.append(
                                f"{self.parse_type(curr_module, operator.input[var_name].value_type)} {var_name}, ")

                return parsed_list

            parsed_str += f"""\
{self.parse_comment_above(operator.comment, tab='    ')}\
    virtual {self.parse_type(curr_module, operator.return_type) if has_return() else 'void'} {operator.name}({''.join(parse_all_vars(True))}ksf::KsfCurrentPtr _current_) = 0;\n\n"""

            parsed_async_str += f"""\
    static void async_response_{operator.name}(ksf::KsfCurrentPtr _current_{''.join(parse_all_vars())})
    {{
        switch (_current_->getRequestVersion()) {{
            case ksf::KUPVERSION: {{
                ksf::kup::UniAttribute<ksf::BufferWriterVector, ksf::BufferReader> _ksfAttr_;
                _ksfAttr_.setVersion(_current_->getRequestVersion());
{parse_output_vars(mode='kup', tab=4)}
                std::vector<char> sKupResponseBuffer;
                _ksfAttr_.encode(sKupResponseBuffer);
                _current_->sendResponse(ksf::KSFSERVERSUCCESS, sKupResponseBuffer);
                break;
            }}\n"""
            if self.with_json:
                parsed_async_str += f"""\
            case ksf::JSONVERSION: {{
                ksf::JsonValueObjPtr _p = new ksf::JsonValueObj();
{parse_output_vars(mode='json', tab=4)}
                std::vector<char> sJsonResponseBuffer;
                ksf::KS_Json::writeValue(_p, sJsonResponseBuffer);
                _current_->sendResponse(ksf::KSFSERVERSUCCESS, sJsonResponseBuffer);
                break;
        }}\n"""
            parsed_async_str += f"""\
            case ksf::KSFVERSION: {{
                ksf::KsfOutputStream<ksf::BufferWriterVector> _os;
{parse_output_vars(mode='ksf', tab=4)}
                _current_->sendResponse(ksf::KSFSERVERSUCCESS, _os);
                break;
            }}
            default: {{std::runtime_error("unsupport ksf packet version");}}
        }} // end switch\n\n"""

            # 链路追踪
            if self.with_trace:
                if not self.with_json:
                    raise SyntaxError("如果需要链路追踪，需要打开生成Json序列化支持(--json)")

                parsed_async_str += f"""\
        if (_current_->isTraced()) {{
            std::string _trace_param_;
            int _trace_param_flag_ = ksf::ServantProxyThreadData::needTraceParam(ksf::ServantProxyThreadData::TraceContext::EST_SS, _current_->getTraceKey(), _rsp_len_);
            if (ksf::ServantProxyThreadData::TraceContext::ENP_NORMAL == _trace_param_flag_) {{
                ksf::JsonValueObjPtr _p_ = new ksf::JsonValueObj();
                {'_p_->value[""] = ksf::JsonOutput::writeJson(_ret);' if has_return() else ''}
                _trace_param_ = ksf::KS_Json::writeValue(_p_);
            }} else if(ksf::ServantProxyThreadData::TraceContext::ENP_OVERMAXLEN == _trace_param_flag_) {{
                _trace_param_ = "{{\"trace_param_over_max_len\":true}}";
            }}
            
            KSF_TRACE(_current_->getTraceKey(), TRACE_ANNOTATION_SS, "", ksf::ServerConfig::Application + "." + ksf::ServerConfig::ServerName, "test", 0, _trace_param_, "");
        }}\n"""
            dispatch_case_str += f"""\
            case {index}: {{
                ksf::KsfInputStream<ksf::BufferReader> _is;
                _is.setBuffer(_current->getRequestBuffer());
{parse_vars_list(tab=4)}
                switch (_current->getRequestVersion()) {{
                    case ksf::KUPVERSION: {{
                        ksf::kup::UniAttribute<ksf::BufferWriterVector, ksf::BufferReader>  _ksfAttr_;
                        _ksfAttr_.setVersion(_current->getRequestVersion());
                        _ksfAttr_.decode(_current->getRequestBuffer());
                        break;
                    }} 
                    case ksf::JSONVERSION: {{
                        ksf::JsonValueObjPtr _jsonPtr = ksf::JsonValueObjPtr::dynamicCast(ksf::KS_Json::getValue(_current->getRequestBuffer()));
                        break;
                    }}
                    default: {{}}
                }}
                
                {f"{self.parse_type(curr_module, operator.return_type)} _ret = " if has_return() else ""}{operator.name}({parse_invoke_vars()}_current);
                if(_current->isResponse()) {{
                    switch (_current->getRequestVersion()) {{
                        case ksf::KUPVERSION: {{
                            ksf::kup::UniAttribute<ksf::BufferWriterVector, ksf::BufferReader>  _ksfAttr_;
                            _ksfAttr_.setVersion(_current->getRequestVersion());
{parse_output_vars(mode='kup', tab=7)}
                            _ksfAttr_.encode(_sResponseBuffer);
                            break;
                        }} 
                        case ksf::JSONVERSION: {{
                            ksf::JsonValueObjPtr _p = new ksf::JsonValueObj();
{parse_output_vars(mode='json', tab=7)}
                            ksf::KS_Json::writeValue(_p, _sResponseBuffer);
                            break;
                        }} 
                        case ksf::KSFVERSION: {{
                            ksf::KsfOutputStream<ksf::BufferWriterVector> _os;
{parse_output_vars(mode='ksf', tab=7)}
                            _os.swap(_sResponseBuffer);
                            break;
                        }}
                        default: {{}}
                    }}
                }}
                return ksf::KSFSERVERSUCCESS;

            }}\n"""
            index += 1

            parsed_async_str += f"""\
    }}
\n"""
            parsed_push_str += f"""\
    static void async_response_push_{operator.name}(ksf::KsfCurrentPtr _current_{''.join(parse_all_vars())}, const std::map<std::string, std::string> &_context = ksf::Current::KSF_STATUS())
    {{
        {{
            ksf::KsfOutputStream<ksf::BufferWriterVector> _os;
{parse_output_vars(mode='ksf', tab=3)}
            _current_->sendPushResponse(ksf::KSFSERVERSUCCESS, "{operator.name}", _os, _context);
        }}
    }}
\n"""

        parsed_str += f"""public:
/*异步应答的封装函数*/\n\n"""
        parsed_str += parsed_async_str

        parsed_str += f"""public:
/*推送应答的封装函数*/\n\n"""

        parsed_str += parsed_push_str

        parsed_str += f"""\
public:
    int onDispatch(ksf::KsfCurrentPtr _current, std::vector<char> &_sResponseBuffer) override
    {{
        static std::string __{ksf_interface.name}_all[] = {{"{'", "'.join(ksf_interface.operator.keys())}"}};
                                            
        std::pair<std::string *, std::string *> r = equal_range(__{ksf_interface.name}_all, __{ksf_interface.name}_all + 9, _current->getFuncName());
        
        if (r.first == r.second) {{
            return ksf::KSFSERVERNOFUNCERR;
        }}
        
        switch (r.first - __{ksf_interface.name}_all) {{
"""

        parsed_str += dispatch_case_str
        parsed_str += f"""\
        }} //end switch
        
        return ksf::KSFSERVERNOFUNCERR;
    }} //end onDispatch\n"""

        parsed_str += f"""}}; // end {ksf_interface.name}\n\n"""
        return parsed_str

    def parse_interface(self, curr_module, ksf_interface: KsfInterface):
        interface_str = ''

        self.add_include("<servant/Agent.h>")
        self.add_include("<servant/Servant.h>")

        interface_str += self.add_lines(self.parse_InterfacePrxCallBack(curr_module, ksf_interface))
        self.add_include("<promise/promise.h>")
        interface_str += self.add_lines(self.parse_InterfacePrxCallbackPromise(curr_module, ksf_interface))
        interface_str += self.parse_InterfaceCoroPrxCallback(curr_module, ksf_interface)
        interface_str += self.parse_InterfaceProxy(curr_module, ksf_interface)
        interface_str += self.parse_InterfaceObj(curr_module, ksf_interface)

        return interface_str

    def to_file(self):
        # 生成头文件（需要判断是否忽略路径)
        for inc, inc_file_name in self.ast_in_file.includes:
            if self.with_ignore_relative_path:
                self.add_include(f'"{inc.name[:-4]}.h"')
            else:
                self.add_include(f'"{inc_file_name[:-4]}.h"')

        curr_module = None
        for ele in self.ast_in_file.elements:
            # 生成命名空间
            if curr_module is None:
                curr_module = ele.module
                self.file_str += self.curr_tab + f"namespace {ele.module} {{\n\n"
            elif curr_module != ele.module:
                curr_module = ele.module
                self.file_str += self.curr_tab + f"}} //end {curr_module}\n\n\nnamespace {ele.module} {{\n\n"

            if isinstance(ele, KsfConst):
                self.file_str += self.parse_const(curr_module, ele)
                pass
            elif isinstance(ele, KsfEnum):
                self.file_str += self.parse_enum(curr_module, ele)
                pass
            elif isinstance(ele, KsfStruct):
                self.file_str += self.parse_struct(curr_module, ele)
                pass
            elif isinstance(ele, KsfInterface) and self.with_rpc:
                self.file_str += self.parse_interface(curr_module, ele)

        self.file_str += f"}} //end {curr_module}\n\n"

        self.file_str = "#pragma once\n\n" + self.parse_header() + "\n\n" + self.file_str
        # print(self.file_str)

        with self.generated_file.open("w") as f:
            f.write(self.file_str)


def cpp_gen(files, include_dirs, destination_dir, flags=None):
    # 读取文件
    # parser_grammar = {}
    if flags is None:
        flags = defaultdict(bool)

    file_path = files

    real_inc_dirs = set()
    for inc in include_dirs:
        real_inc_dirs.add(str(Path(inc).resolve()))
    ast = generate(file_path, real_inc_dirs, flags['with_current_priority'])
    for file in file_path:
        CppGenerator(ast, file, destination_dir, **flags).to_file()


# 测试用例
if __name__ == '__main__':
    file_path = [
        'example/enum_simple.ksf',
        'example/const_definition.ksf',
        'example/struct_simple.ksf'
    ]

    include_dirs = ['../../']

    destination_dir = '../../gen'

    cpp_gen(file_path, include_dirs, destination_dir)
