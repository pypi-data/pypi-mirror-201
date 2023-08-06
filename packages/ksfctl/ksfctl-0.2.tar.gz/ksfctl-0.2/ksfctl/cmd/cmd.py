import os

import click

from ksfctl.generate.cpp_generator import cpp_gen


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.pass_context
def cli(ctx):
    pass


@cli.group(name='parse', help="解析ksf文件到其他语言，目前支持(cpp, python, java, node.js, go)", context_settings={'help_option_names': ['-h', '--help']})
@click.pass_context
def parse(ctx):
    pass


@parse.command(name='cpp', context_settings={'help_option_names': ['-h', '--help']})
@click.pass_context
@click.argument('ksf_files', nargs=-1, required=True, type=str)
@click.option('-i', '--include', '--include-path', multiple=True, help='ksf协议文件搜索路径')
@click.option('-d', '--dir', '--dest', 'destination_dir', multiple=False, help='生成的头文件存放的路径')
@click.option('--replace_ns', '--replace-ns', multiple=False, help='(将被废弃)替换namespace')
@click.option('--replace-namespace', nargs=2, multiple=True, type=str, help='(推荐)将指定命名空间替换为另一个命名空间')
@click.option('--replace-include-dir', nargs=2, multiple=True, type=str, help='(推荐)替换头文件路径')
@click.option('--ignore-relative-path', 'ignore_relative_path', is_flag=True, flag_value=True, default=False, help='忽略依赖目录')
@click.option('--check-default/--no-check-default', default=True, help='是否打包默认值')
@click.option('--ksf/--no-ksf', 'ksf', is_flag=True, default=False, help='是否ksf内部模块')
@click.option('--json/--no-json', 'json', is_flag=True, default=True, help='是否生成Json格式')
@click.option('--sql/--no-sql', 'sql', is_flag=True, default=False, help='是否生成Sql接口')
@click.option('--rpc/--no-rpc', 'rpc', is_flag=True, default=True, help='是否生成RPC接口')
@click.option('--current-priority/--no-current-priority', 'current_priority', is_flag=True, default=True,
              help='是否优先使用当前目录')
@click.option('--trace/--no-trace', 'trace', is_flag=True, default=False, help='是否需要调用链追踪逻辑')
@click.option('--push/--no-push', 'push', is_flag=True, default=True, help='是否需要推送接口')
@click.option('--param-rvalue-ref/--no-param-rvalue-ref', 'param_rvalue_ref', is_flag=True, default=False,
              help='是否参数使用右值引用')
@click.option('--with-ksf', 'ksf', is_flag=True, flag_value=True, default=False, help='ksf内部模块')
@click.option('--unjson', 'json', is_flag=True, flag_value=False, default=True, help='不生成Json格式')
@click.option('--os', 'rpc', is_flag=True, default=True, flag_value=False, help='不生成RPC接口')
@click.option('--currentPriority', 'current_priority', is_flag=True, flag_value=True, default=True,
              help='优先使用当前目录')
@click.option('--without-trace', 'trace', is_flag=True, flag_value=False, default=False, help='不需要调用链追踪')
@click.option('--with-push', 'push', is_flag=True, flag_value=True, default=True, help='需要推送接口')
@click.option('--with-param-rvalue-ref', 'param_rvalue_ref', is_flag=True, flag_value=True, default=False,
              help='参数使用右值引用')
def parse_cpp(ctx, ksf_files, include, destination_dir, replace_ns, replace_namespace, replace_include_dir, **kwargs):
    ctx.help_option_names += ['-h']
    """命令的描述"""
    click.echo(f'文件列表: {ksf_files}')

    """将指定命名空间替换为另一个命名空间"""
    if replace_namespace:
        for ns in replace_namespace:
            origin, actual = ns
            click.echo(f'将命名空间 {origin} 替换为 {actual}。')
    elif replace_ns:
        replace_namespace = []
        for replace_namespace_str in replace_ns.split(";"):
            origin, actual = replace_namespace_str.split("/")
            replace_namespace.append((origin, actual))
            click.echo(f'将命名空间 {origin} 替换为 {actual}。')
    else:
        click.echo('未指定任何命名空间的置换。')

    """替换头文件路径"""
    if replace_include_dir:
        for ns in replace_namespace:
            origin, actual = ns
            click.echo(f'将头文件路径 {origin} 替换为 {actual}。')
    else:
        click.echo('未指定任何头文件路径的置换。')

    """生成文件位置"""
    if destination_dir:
        click.echo(f'生成文件位置: {destination_dir}')
    else:
        destination_dir = os.getcwd()
        click.echo(f'生成文件位置: {destination_dir}')

    """头文件包含路径"""
    if include:
        click.echo(f'包含路径: {include}')
    else:
        click.echo(f'未指定包含路径，将只在当前路径搜索')

    """是否检测默认值"""
    click.echo(f"是否检测默认值：{kwargs['check_default']}")

    """是否ksf内部模块"""
    click.echo(f"是否ksf内部模块：{kwargs['ksf']}")

    """是否生成Json序列化接口"""
    click.echo(f"是否生成Json序列化接口：{kwargs['json']}")

    """是否生成Sql接口"""
    click.echo(f"是否生成Sql接口：{kwargs['sql']}")

    """是否生成RPC接口"""
    click.echo(f"是否生成RPC接口：{kwargs['rpc']}")

    """是否优先使用当前目录"""
    click.echo(f"是否优先使用当前目录：{kwargs['current_priority']}")

    """是否需要调用链追踪逻辑"""
    click.echo(f"是否需要调用链追踪逻辑：{kwargs['trace']}")

    """是否参数使用右值引用"""
    click.echo(f"是否参数使用右值引用：{kwargs['param_rvalue_ref']}")

    """忽略依赖目录"""
    click.echo(f"忽略依赖目录：{kwargs['ignore_relative_path']}")

    """解析所有的flags，携带with_头"""
    kwargs_with_prefix = {}
    for k, v in kwargs.items():
        kwargs_with_prefix.update({f'with_{k}': v})

    cpp_gen(files=ksf_files, include_dirs=include, destination_dir=destination_dir, flags=kwargs_with_prefix)


if __name__ == '__main__':
    cli()
    exit(0)

    runner = CliRunner()
    result1 = runner.invoke(cli, ['-h'])
    assert result1.exit_code == 0

    result2 = runner.invoke(cli, ['--help'])
    assert result2.exit_code == 0


