import subprocess
from os import mkdir, path
from typing import cast
from sys import stdout

from constants import (
    ASSERT_MD_STRUCT,
    ASSIGN_MD_STRUCT,
    CLASS_DEF_MD_STRUCT,
    DEFAULT_MKDOCS_YML,
    FILE_MARKDOWN,
    FUNCTION_DEF_MD_STRUCT,
    IMPORT_MD_STRUCT,
)
from custom_types import CodebaseDict, ImportType, Lang, StandardReturn, Statement
from utils import indent_code


def generate_doc(
    codebase: CodebaseDict,
    root: str,
    exit: str,
    proj_name: str,
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
        stdout.write(result.stdout)
    except subprocess.CalledProcessError as e:
        stdout.write(f'Error: {e.stderr}')

    with open(path.join(exit_path, 'mkdocs.yml'), 'w', encoding='utf-8') as f:
        f.write(
            default_doc_config(
                proj_name,
                edit_uri,
                repo_name,
                repo_url,
            )
        )

    process_codebase(codebase, root, exit)


def default_doc_config(
    proj_name: str,
    edit_uri: str,
    repo_name: str = 'GitHub',
    repo_url: str = '',
) -> str:
    return DEFAULT_MKDOCS_YML.format(
        proj_name=proj_name,
        edit_uri=edit_uri,
        repo_name=repo_name,
        repo_url=repo_url,
    )


def codebase_file_to_markdown(filedata: list[StandardReturn], basedir: str) -> str:
    filename: str = basedir.split(path.sep)[-1]
    filepath: str = (
        basedir.removesuffix(filename).replace(path.sep, '.').removesuffix('.')
    )
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
                raise NotImplementedError('Should not fallback to this.')

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
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    return IMPORT_MD_STRUCT.format(
        name=name,
        _path=_path,
        category=category,
        code=code,
    )


def handle_import_from(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    _path: str = cast(str, stmt['path'])
    category: str = cast(ImportType, stmt['category']).value
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    return IMPORT_MD_STRUCT.format(
        name=name,
        _path=_path,
        category=category,
        code=code,
    )


def handle_assign(stmt: StandardReturn) -> str:
    tokens: str = ', '.join(cast(list[str], stmt['tokens']))
    _type: str = 'Unknown'
    value: str = cast(str, stmt['value'])
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    return ASSIGN_MD_STRUCT.format(
        token=tokens,
        _type=_type,
        value=value,
        code=code,
    )


def handle_annassign(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    annot: str = cast(str, stmt['annot'])
    value: str = cast(str, stmt['value'])
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    return ASSIGN_MD_STRUCT.format(
        token=name,
        _type=annot,
        value=value,
        code=code,
    )


def handle_class_def(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    inherit: str = ', '.join(cast(list[str], stmt['inheritance']))
    decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
    kwargs: str = cast(str, stmt['kwargs'])
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    return CLASS_DEF_MD_STRUCT.format(
        name=name,
        inherit=inherit,
        decorators=decorators,
        kwargs=kwargs,
        code=code,
    )


def handle_function_def(stmt: StandardReturn) -> str:
    name: str = cast(str, stmt['name'])
    decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
    args: str = cast(str, stmt['args'])
    kwargs: str = cast(str, stmt['kwargs'])
    rtype: str = cast(str, stmt['rtype'])
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    return FUNCTION_DEF_MD_STRUCT.format(
        name=name,
        decorators=decorators,
        args=args,
        kwargs=kwargs,
        rtype=rtype,
        code=code,
    )


def handle_assert(stmt: StandardReturn) -> str:
    test: str = cast(str, stmt['test'])
    msg: str = cast(str, stmt['msg'])
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    return ASSERT_MD_STRUCT.format(test=test, msg=msg, code=code)


def process_codebase(
    codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]],
    root: str,
    exit: str,
    basedir: str = '',
):
    parents: list[str] = list(codebase.keys())

    for key in parents:
        value = codebase[key]
        new_path: str = path.join(basedir, key)

        if isinstance(value, list):
            if len(value):
                content: str = codebase_file_to_markdown(value, new_path)

                output_file_path: str = path.join(
                    exit, 'docs', new_path.removeprefix(root) + '.md'
                )
                folder_path = output_file_path.split(key)[0]
                if not path.exists(folder_path):
                    mkdir(folder_path)
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        else:
            process_codebase(value, root, exit, new_path)
