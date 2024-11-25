import subprocess
from os import path
from typing import cast

from constants import DEFAULT_MKDOCS_YML, FILE_MARKDOWN
from custom_types import CodebaseDict, ImportType, Lang, StandardReturn, Statement


def generate_doc(
    codebase: CodebaseDict,
    exit: str,
    proj_name: str,
    lang: Lang,
    edit_uri: str = '',
    repo_name: str = 'GitHub',
    repo_url: str = '',
) -> None:
    exit_path: str = path.abspath(exit)

    try:
        result = subprocess.run(
            ['mkdocs', 'new', exit_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print('Error:', e.stderr)

    with open(path.join(exit_path, 'mkdocs.yml'), 'w', encoding='utf-8') as f:
        f.write(
            default_doc_config(
                proj_name,
                edit_uri,
                lang.value,
                repo_name,
                repo_url,
            )
        )

    process_codebase(codebase)


def default_doc_config(
    proj_name: str,
    edit_uri: str,
    lang: str,
    repo_name: str = 'GitHub',
    repo_url: str = '',
) -> str:
    return DEFAULT_MKDOCS_YML.format(
        proj_name=proj_name,
        edit_uri=edit_uri,
        lang=lang,
        repo_name=repo_name,
        repo_url=repo_url,
    )


def codebase_file_to_markdown(filedata: list[StandardReturn], basedir: str) -> str:
    filename: str = basedir.split(path.sep)[-1]
    filepath: str = basedir.removesuffix(filename).replace(path.sep, '.')
    filedoc: str = ''
    imports: str = ''
    constants: str = ''
    classes: str = ''
    functions: str = ''
    assertions: str = ''

    for stmt in filedata:
        match stmt['statement']:
            case Statement.Import:
                imports += handle_import(stmt)

            case Statement.ImportFrom:
                imports += handle_import_from(stmt)

            case Statement.Assign:
                constants += handle_assign(stmt)

            case Statement.AnnAssign:
                constants += handle_annassign(stmt)

            case Statement.ClassDef:
                classes += handle_class_def(stmt)

            case Statement.FunctionDef | Statement.AsyncFunctionDef:
                functions += handle_function_def(stmt)

            case Statement.Assert:
                assertions += handle_assert(stmt)

            case _:
                print('passed')

    return FILE_MARKDOWN.format(
        filename=filename,
        filepath=filepath,
        filedoc=filedoc,
        imports=imports,
        constants=constants,
        classes=classes,
        functions=functions,
        assertions=assertions,
    )


def handle_import(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    _path: None = None
    category: str = cast(ImportType, stmt['category']).value
    code: str = cast(str, stmt['code'])

    return f'### `{name}`\n\nPath: `#!py {_path}`\n\nCategory: {category}\n\n??? example "SNIPPET":\n\n```py\n{code}\n```\n\n'


def handle_import_from(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    _path: str = cast(str, stmt['path'])
    category: str = cast(ImportType, stmt['category']).value
    code: str = cast(str, stmt['code'])

    return f'### `{name}`\n\nPath: `#!py {_path}`\n\nCategory: {category}\n\n??? example "SNIPPET":\n\n```py\n{code}\n```\n\n'


def handle_assign(stmt: StandardReturn) -> str:
    tokens: str = ', '.join(cast(list[str], stmt['tokens']))
    value: str = cast(str, stmt['value'])
    code: str = cast(str, stmt['code'])

    return f'### `{tokens}`\n\nType: `Unknown`\n\nValue: `#!py {value}`\n\n??? example "SNIPPET":\n\n```py\n{code}\n```\n\n'


def handle_annassign(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    annot: str = cast(str, stmt['annot'])
    value: str = cast(str, stmt['value'])
    code: str = cast(str, stmt['code'])

    return f'### `{name}`\n\nType: `#!py {annot}`\n\nValue: `#!py {value}`\n\n??? example "SNIPPET":\n\n```py\n{code}\n```\n\n'


def handle_class_def(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    inherit: str = ', '.join(cast(list[str], stmt['inheritance']))
    decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
    kwargs: str = cast(str, stmt['kwargs'])
    code: str = cast(str, stmt['code'])

    return f'### `{name}`\n\nParents: `{inherit}`\n\nDecorators: `#!py {decorators}`\n\nKwargs: {kwargs}\n\n??? example "SNIPPET":\n\n```py\n{code}\n```\n\n'


def handle_function_def(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
    args: str = cast(str, stmt['args'])
    kwargs: str = cast(str, stmt['kwargs'])
    rtype: str = cast(str, stmt['rtype'])
    code: str = cast(str, stmt['code'])

    return f'### `{name}`\n\nType: `#!py ...`\n\nReturn Type: {rtype}\n\nDecorators: `#!py {decorators}`\n\nArgs: {args}\n\nKwargs: {kwargs}\n\n??? example "SNIPPET":\n\n```py\n{code}\n```\n\n'


def handle_assert(stmt: StandardReturn) -> str:
    test: str = cast(str, stmt['test'])
    msg: str = cast(str, stmt['msg'])
    code: str = cast(str, stmt['code'])

    return f'### `#!py assert {test}, {msg}`\n\n??? example "SNIPPET":\n\n```py\n{code}\n```\n\n'


def process_codebase(
    codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]],
    basedir: str = '',
):
    parents: list[str] = list(codebase.keys())

    for key in parents:
        value = codebase[key]
        new_path: str = path.join(basedir, key)

        if isinstance(value, list):
            if len(value):
                content: str = codebase_file_to_markdown(value, new_path)
                print(content)
            # Add to mkdos.yml > nav
            # Add to doc .md file
        else:
            process_codebase(value, new_path)
