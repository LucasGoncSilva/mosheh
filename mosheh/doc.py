import subprocess
from os import mkdir, path
from sys import stdout
from typing import cast

from constants import (
    ASSERT_MD_STRUCT,
    ASSIGN_MD_STRUCT,
    CLASS_DEF_MD_STRUCT,
    DEFAULT_MKDOCS_YML,
    FILE_MARKDOWN,
    FUNCTION_DEF_MD_STRUCT,
    IMPORT_MD_STRUCT,
)
from custom_types import CodebaseDict, ImportType, StandardReturn, Statement
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
    """
    Generates a documentation structure for a Python codebase using MkDocs.

    This function creates a new MkDocs project at the specified output path, writes a
    configuration file, and processes the provided codebase to generate documentation.

    Key concepts:
    - MkDocs: A static site generator that's geared towards project documentation.
    - Codebase Processing: The function relies on `process_codebase` to handle the
      codebase structure and populate the documentation content based on Python files
      and their statements.
    - Configuration: Builds a `mkdocs.yml` configuration file with project details,
      including repository information and editing URI.

    :param codebase: dict containing nodes representing `.py` files and their stmts
    :type codebase: CodebaseDict
    :param root: the root path of the source code to be documented
    :type root: str
    :param exit: the output dir where the documentation will be generated
    :type exit: str
    :param proj_name: the name of the project, for generating MkDocs configuration
    :type proj_name: str
    :param edit_uri: optional URI for linking to source file edits (defaults to '')
    :type edit_uri: str, optional
    :param repo_name: the repository provider name (defaults to 'GitHub')
    :type repo_name: str, optional
    :param repo_url: the URL of the repository, used for linking in the documentation
    :type repo_url: str, optional
    :return: nothing, just generates documentation files in the specified output path
    :rtype: None
    """

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


def codebase_to_markdown(filedata: list[StandardReturn], basedir: str) -> str:
    """
    Converts a file's processed data into a structured Markdown representation.

    This function processes a list of statements extracted from a Python file and
    generates a Markdown-formatted string. It categorizes statements into imports,
    constants, classes, functions, and assertions, ensuring that each type is
    documented appropriately. If a category has no statements, a default informational
    message is added.

    Key concepts:
    - Statement Handling: The function processes different types of statements
      (imports, assignments, class and function definitions, etc.) and organizes
      them into corresponding sections.
    - Markdown Generation: The output is formatted using a predefined Markdown
      template (`FILE_MARKDOWN`) that structures the documentation by category.
    - Category Defaults: If no statements exist for a particular category, an
      informational block is added to indicate its absence.

    Example:
    ```python
    filedata: list[StandardReturn] = [
        {'statement': Statement.Import, 'name': 'os', ...},
        {'statement': Statement.ClassDef, 'name': 'MyClass', ...},
    ]
    markdown_doc: str = codebase_to_markdown(filedata, '/path/to/module/file.py')
    markdown_doc
    # Outputs a Markdown string with sections for imports and classes
    ```

    :param filedata: a list of statement dict for the parsed contents of a Python file
    :type filedata: list[StandardReturn]
    :param basedir: the file in-process' base dir, used to generate the module path
    :type basedir: str
    :return: a Markdown-formatted string documenting the contents of the file
    :rtype: str
    """

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

    if not len(imports):
        imports = '!!! info "NO IMPORT DEFINED HERE"'
    if not len(constants):
        constants = '!!! info "NO CONSTANT DEFINED HERE"'
    if not len(classes):
        classes = '!!! info "NO CLASS DEFINED HERE"'
    if not len(functions):
        functions = '!!! info "NO FUNCTION DEFINED HERE"'
    if not len(assertions):
        assertions = '!!! info "NO ASSERT DEFINED HERE"'

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
    """
    Generates a Markdown representation for an import statement.

    This function processes an `import` statement from a parsed Python file, formatting
    it into a structured Markdown block. The output includes the import name, category,
    and the indented code snippet.

    Key concepts:
    - Import Handling: Extracts the import statement's details (name, category, code)
      and formats them for documentation.
    - Indentation: The `indent_code` function is used to apply consistent indentation
      to the statement code before including it in the Markdown output.
    - MD Struct: The output Markdown uses a predefined template - `IMPORT_MD_STRUCT`.

    Example:
    ```python
    stmt: StandardReturn = {
        'statement': Statement.Import,
        'name': 'os',
        'category': ImportType.Native,
        'code': 'import os',
    }
    markdown_import: str = handle_import(stmt)
    markdown_import
    # Outputs a formatted Markdown string representing the import
    ```

    :param stmt: a dict containing the details of the import statement
    :type stmt: StandardReturn
    :return: a formatted Markdown string documenting the import statement
    :rtype: str
    """

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
    """
    Generates a Markdown representation for an import statement.

    This function processes a `from ... import ...` statement from a parsed Python
    file, formatting it into a structured Markdown block. The output includes the
    import name, category, and the indented code snippet.

    Key concepts:
    - Import Handling: Extracts the import statement's details (name, category, code)
      and formats them for documentation.
    - Indentation: The `indent_code` function is used to apply consistent indentation
      to the statement code before including it in the Markdown output.
    - MD Struct: The output Markdown uses a predefined template - `IMPORT_MD_STRUCT`.

    Example:
    ```python
    stmt: StandardReturn = {
        'statement': Statement.ImportFrom,
        'name': 'environ',
        'category': ImportType.Native,
        'code': 'from os import environ',
    }
    markdown_import: str = handle_import(stmt)
    markdown_import
    # Outputs a formatted Markdown string representing the import
    ```

    :param stmt: a dict containing the details of the import statement
    :type stmt: StandardReturn
    :return: a formatted Markdown string documenting the import statement
    :rtype: str
    """

    name: str = cast(str, stmt['name'])
    _path: str = cast(str, stmt['path'])
    category: str = cast(ImportType, stmt['category']).value
    code: str = indent_code(f'from {_path} import {name}')

    return IMPORT_MD_STRUCT.format(
        name=name,
        _path=_path,
        category=category,
        code=code,
    )


def handle_assign(stmt: StandardReturn) -> str:
    """
    Generates a Markdown representation for an `assign` statement.

    This function processes an assign statement from a parsed Python file, formatting
    it into a structured Markdown block. The output includes the assign name, category,
    and the indented code snippet.

    Key concepts:
    - Import Handling: Extracts the assign statement's details (tokens, value, code)
      and formats them for documentation.
    - Indentation: The `indent_code` function is used to apply consistent indentation
      to the statement code before including it in the Markdown output.
    - MD Struct: The output Markdown uses a predefined template - `ASSIGN_MD_STRUCT`.

    Example:
    ```python
    stmt: StandardReturn = {
        'statement': Statement.Assign,
        'tokens': ['foo', 'bar'],
        'value': '(True, False)',
        'code': 'foo, bar = True, False',
    }
    markdown_assign: str = handle_assign(stmt)
    markdown_assign
    # Outputs a formatted Markdown string representing the assign
    ```

    :param stmt: a dict containing the details of the assign statement
    :type stmt: StandardReturn
    :return: a formatted Markdown string documenting the assign statement
    :rtype: str
    """

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
    """
    Generates a Markdown representation for a `var: type = value` statement.

    This function processes an annotated assign statement from a parsed Python file,
    formatting into a structured Markdown block. The output includes the assign name,
    category, and the indented code snippet.

    Key concepts:
    - Import Handling: Extracts the assign statement's details (name, annot, value,
      code) and formats them for documentation.
    - Indentation: The `indent_code` function is used to apply consistent indentation
      to the statement code before including it in the Markdown output.
    - MD Struct: The output Markdown uses a predefined template - `ASSIGN_MD_STRUCT`.

    Example:
    ```python
    stmt: StandardReturn = {
        'statement': Statement.AnnAssign,
        'name': 'var',
        'annot': 'str',
        'value': '"example"',
        'code': 'var: str = "example"',
    }
    markdown_annassign: str = handle_annassign(stmt)
    markdown_annassign
    # Outputs a formatted Markdown string representing the annotated assign
    ```

    :param stmt: a dict containing the details of the annassign statement
    :type stmt: StandardReturn
    :return: a formatted Markdown string documenting the annassign statement
    :rtype: str
    """

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
    """
    Generates a Markdown representation for a `class` definition statement.

    This function processes a class definition from a parsed Python codebase,
    extracting key details such as the class name, inheritance, decorators,
    keyword arguments, and the code itself. It formats this information into
    a structured Markdown block for documentation purposes.

    Key concepts:
    - Class Handling: Extracts information about the class, including its name,
      inheritance hierarchy, and decorators.
    - Indentation: Applies consistent indentation to the class code using the
      `indent_code` function.
    - Markdown Structure: Utilizes a predefined template (`CLASS_DEF_MD_STRUCT`)
      to format the class details in Markdown.

    Example:
    ```python
    stmt: StandardReturn = {
        'statement': Statement.ClassDef,
        'name': 'MyClass',
        'inheritance': ['BaseClass'],
        'decorators': ['@dataclass'],
        'kwargs': '',
        'code': 'class MyClass(BaseClass):',
    }
    markdown_class: str = handle_class_def(stmt)
    markdown_class
    # Outputs a formatted Markdown string representing the class definition
    ```

    :param stmt: a dict containing the details of the class definition statement
    :type stmt: StandardReturn
    :return: a formatted Markdown string documenting the class definition
    :rtype: str
    """

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
    """
    Generates a Markdown representation for a function definition statement.

    This function processes a function or method definition from a parsed Python
    codebase, extracting details such as the function name, decorators, arguments,
    keyword arguments, return type, and the code itself. It formats this information
    into a structured Markdown block for documentation purposes.

    Key concepts:
    - Function Handling: Extracts the function's metadata, including decorators,
      arguments, and return type.
    - Indentation: Applies consistent indentation to the function code using the
      `indent_code` function.
    - Markdown Structure: Utilizes a predefined template (`FUNCTION_DEF_MD_STRUCT`)
      to format the function details in Markdown.

    Example:
    ```python
    stmt: StandardReturn = {
        'statement': Statement.FunctionDef,
        'name': 'sum_thing',
        'decorators': ['@staticmethod'],
        'args': [('x', 'int', None), ('y', 'int', None)],
        'kwargs': [],
        'rtype': 'int',
        'code': 'def sum_thing(x: int, y: int) -> int: return x + y',
    }
    markdown_function: str = handle_function_def(stmt)
    markdown_function
    # Outputs a formatted Markdown string representing the function definition
    ```

    :param stmt: a dict containing the details of the function definition statement
    :type stmt: StandardReturn
    :return: a formatted Markdown string documenting the function definition
    :rtype: str
    """

    name: str = cast(str, stmt['name'])
    decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
    args: str = cast(str, stmt['args'])
    kwargs: str = cast(str, stmt['kwargs'])
    rtype: str = cast(str, stmt['rtype']) or 'Unknown'
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
    """
    Generates a Markdown representation for an `assert x` statement.

    This function processes an assert statement from a parsed Python codebase,
    extracting the test condition, optional message, and the code itself. It formats
    this information into a structured Markdown block for documentation purposes.

    Key concepts:
    - Assertion Handling: Extracts the test condition and message from the assert
      statement.
    - Indentation: Applies consistent indentation to the assert code using the
      `indent_code` function.
    - Markdown Structure: Utilizes a predefined template (`ASSERT_MD_STRUCT`)
      to format the assertion details in Markdown.

    Example:
    ```python
    stmt: StandardReturn = {
        'statement': Statement.Assert,
        'test': 'x > 0',
        'msg': '"x must be positive"',
        'code': 'assert x > 0, "x must be positive"',
    }
    markdown_assert: str = handle_assert(stmt)
    markdown_assert
    # Outputs a formatted Markdown string representing the assert statement
    ```

    :param stmt: A dictionary containing the details of the assert statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the assert statement.
    :rtype: str
    """

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
) -> None:
    """
    Recursively processes a CodebaseDict generating `.mf` files for each module

    This function traverses the codebase, converting the content of each Python file
    (represented as a list of statements) into a Markdown file. It maintains the folder
    structure, creating necessary directories and writing the corresponding `.md` files
    to the specified output path.

    Example:
    ```python
    codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]] = {
        'module1.py': [{'statement': Statement.ClassDef, 'name': 'MyClass', ...}],
        'subdir': {
            'module2.py': [{
                'statement': Statement.FunctionDef, 'name': 'my_function', ...
            }]
        }
    }
    process_codebase(codebase, '/path/to/source', '/path/to/docs')
    # Generates docs in '/path/to/docs/docs/module1.md' and 'subdir/module2.md'
    ```

    :param codebase: a dictionary representing the codebase structure, where keys are
                    file or dir names, and values are either subdirectories or lists
                    of parsed statements
    :type codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]]
    :param root: the root path of the source code being processed
    :type root: str
    :param exit: the output dir where the Markdown documentation will be generated
    :type exit: str
    :param basedir: the base dir for the current level of the codebase, used
                    for maintaining the folder structure in the output
    :type basedir: str, optional
    :return: nothing, just generates `.md` files in the specified output path
    :rtype: None
    """

    parents: list[str] = list(codebase.keys())

    for key in parents:
        value = codebase[key]
        new_path: str = path.join(basedir, key)

        if isinstance(value, list):
            if len(value):
                content: str = codebase_to_markdown(value, new_path)

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
