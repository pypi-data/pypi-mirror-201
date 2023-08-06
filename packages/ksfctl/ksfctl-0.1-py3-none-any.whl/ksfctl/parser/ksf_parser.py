from collections import defaultdict
from pathlib import Path


class KsfFile:
    def __init__(self, file):
        self.file = file
        self.elements = []
        self.includes = []

    def add_enum(self, enum):
        self.elements.append(enum)

    def add_interface(self, interface):
        self.elements.append(interface)

    def add_struct(self, struct):
        self.elements.append(struct)

    def add_const(self, const):
        self.elements.append(const)

    def add_include(self, inc):
        self.includes.append(inc)


class KsfEnumMember:
    def __init__(self, file, module, enum, name, value, comment=''):
        self.file = file
        self.module = module
        self.name = name
        self.enum = enum
        self.value = value
        self.comment = comment

        self.id = '.'.join([self.module, self.enum, self.name])


class KsfEnum:
    def __init__(self, file, module, name, member, comment=None):
        self.file = file
        self.module = module
        self.name = name
        self.comment = comment
        self.member = []
        for m in member:
            ksf_enum_member = KsfEnumMember(file, module, name, m['name'], m['value'], m['comment'])
            self.member.append(ksf_enum_member)

        self.id = '.'.join([self.module, self.name])


class KsfField:
    def __init__(self, file, module, struct, tag, is_required, value_type, name, default, comment=None):
        self.file = file
        self.module = module
        self.struct = struct
        self.tag = tag
        self.is_required = is_required
        self.value_type = value_type
        self.name = name
        self.default = default
        self.comment = comment

        self.id = '.'.join([self.module, self.struct, self.name])


class KsfStruct:
    def __init__(self, file, module, name, variable, comment=None):
        self.key_fields = []
        self.file = file
        self.module = module
        self.name = name
        self.comment = comment
        self.variable = {}
        for v in variable:
            ksf_field = KsfField(file, module, name, v['tag'], v['is_required'], v['value_type'], v['name'],
                                 v['default'] if 'default' in v else None, v['comment'])
            self.variable[ksf_field.id] = ksf_field

        self.id = '.'.join([self.module, self.name])

    def add_key(self, arg: list):
        self.key_fields = arg


class KsfVariable:
    def __init__(self, file, module, interface, operator, value_type, name, index):
        self.file = file
        self.module = module
        self.interface = interface
        self.operator = operator
        self.value_type = value_type
        self.name = name
        self.index = index

        self.id = '.'.join([self.module, self.interface, self.operator, self.name])


class KsfOperator:
    def __init__(self, file, module, interface, name, return_type, variable, comment=None):
        self.file = file
        self.module = module
        self.interface = interface
        self.name = name
        self.return_type = return_type
        self.comment = comment

        self.input = {}
        self.output = {}
        self.ordered_var = []

        index = 1
        for v in variable:
            ksf_variable = KsfVariable(file, module, interface, name, v['value_type'], v['name'], index)
            if v['is_output']:
                self.ordered_var.append((ksf_variable.name, True))
                self.output[ksf_variable.name] = ksf_variable
            else:
                self.ordered_var.append((ksf_variable.name, False))
                self.input[ksf_variable.name] = ksf_variable

            index += 1

        self.id = '.'.join([self.module, self.interface, self.name])


class KsfInterface:
    def __init__(self, file, module, name, operator, comment=None):
        self.file = file
        self.module = module
        self.name = name
        self.comment = comment
        self.operator = {}

        for o in operator:
            ksf_operator = KsfOperator(file, module, name, o['name'], o['return_type'], o['variable'], o['comment'])
            self.operator[ksf_operator.name] = ksf_operator

        self.id = '.'.join([self.module, self.name])


class KsfConst:
    def __init__(self, file, module, name, value_type, value, comment=''):
        self.file = file
        self.module = module
        self.name = name
        self.value_type = value_type
        self.value = value
        self.comment = comment

        self.id = '.'.join([self.module, self.name])


class KsfBuildInType:
    def __init__(self, name):
        self.id = 'BuildInType.' + name
        self.name = name


class KsfMapType:
    def __init__(self, name, key_type, value_type):
        self.key_type = key_type
        self.value_type = value_type
        super().__init__('MapType.' + name, name)


class KsfVectorType:
    def __init__(self, name, element_type):
        self.element_type = element_type
        super().__init__('VectorType.' + name, name)


class KsfStructType:
    def __init__(self, identity, name, fields, comment='', *args, **kwargs):
        super().__init__(identity, name, *args, **kwargs)
        self.fields = fields
        self.comment = comment


class KsfArrayType:
    pass


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class Ksf:
    natives = {
        "string": KsfBuildInType(name='string'),
        "int": KsfBuildInType(name='int'),
        "uint": KsfBuildInType(name='uint'),
        "bool": KsfBuildInType(name='bool'),
        "short": KsfBuildInType(name='int'),
        "ushort": KsfBuildInType(name='ushort'),
        "long": KsfBuildInType(name='long'),
        "float": KsfBuildInType(name='float'),
        "double": KsfBuildInType(name='double'),
        "byte": KsfBuildInType(name='byte'),
    }

    files = {}

    file2module = defaultdict(list)
    module2file = defaultdict(list)

    enums = {}
    file2enum = defaultdict(list)  # 文件到枚举的映射
    module2enum = defaultdict(list)  # 模块到枚举的映射

    structs = {}
    file2struct = defaultdict(list)  # 文件到结构体的映射
    module2struct = defaultdict(list)  # 模块到结构体的映射

    interfaces = {}
    file2interface = defaultdict(list)  # 文件到接口的映射
    module2interface = defaultdict(list)  # 模块到接口的映射

    consts = {}
    file2const = defaultdict(list)  # 文件到常量的映射
    module2const = defaultdict(list)  # 模块到常量的映射

    all_elements = []

    @classmethod
    def add_enum(cls, ksf_enum: KsfEnum):
        cls.enums[ksf_enum.id] = ksf_enum
        cls.file2enum[ksf_enum.file].append(ksf_enum.id)
        cls.module2enum[ksf_enum.module].append(ksf_enum.id)
        cls.files[ksf_enum.file].add_enum(ksf_enum)
        cls.all_elements.append(ksf_enum)

    @classmethod
    def add_struct(cls, ksf_struct: KsfStruct):
        cls.structs[ksf_struct.id] = ksf_struct
        cls.file2struct[ksf_struct.file].append(ksf_struct.id)
        cls.module2struct[ksf_struct.module].append(ksf_struct.id)
        cls.files[ksf_struct.file].add_struct(ksf_struct)
        cls.all_elements.append(ksf_struct)

    @classmethod
    def add_interface(cls, ksf_interface: KsfInterface):
        cls.interfaces[ksf_interface.id] = ksf_interface
        cls.file2interface[ksf_interface.file].append(ksf_interface.id)
        cls.module2interface[ksf_interface.module].append(ksf_interface.id)
        cls.files[ksf_interface.file].add_interface(ksf_interface)
        cls.all_elements.append(ksf_interface)

    @classmethod
    def add_struct_key(cls, module, struct, arg):
        cls.structs[module + '.' + struct].add_key(arg)

    @classmethod
    def add_constant(cls, ksf_const: KsfConst):
        cls.consts[ksf_const.id] = ksf_const
        cls.file2interface[ksf_const.file].append(ksf_const.id)
        cls.module2interface[ksf_const.module].append(ksf_const.id)
        cls.files[ksf_const.file].add_const(ksf_const)
        cls.all_elements.append(ksf_const)

    @classmethod
    def add_file(cls, file: Path):
        ksf_file = KsfFile(file)
        cls.files[file.name] = ksf_file

    @classmethod
    def add_include(cls, file: Path, include: Path):
        cls.files[file.name].add_include(include)