"""
Containing the logic and functions shared between the commands, more specifically the
logic and functions related to documentation creation/updating.

Two main functions are defined and exported here:

- `process_codebase`: Recursively processes a codebase and generates documentation for
    each file.
- `get_update_set_nav`: Sets the `mkdocs.yml` Nav "Codebase" section to the current
    state, updating it.

Every other function is a private/internal one, being called only for the other ones
from this same file; this is to keep the logic in the same space, while keeping the
code base less confusing.
"""

from logging import Logger, getLogger
from os import makedirs, path, sep
from typing import Any, cast

import yaml

from mosheh.constants import (
    ASSERT_MD_STRUCT,
    ASSIGN_MD_STRUCT,
    CLASS_DEF_MD_STRUCT,
    FILE_MARKDOWN,
    FUNCTION_DEF_MD_STRUCT,
    IMPORT_MD_STRUCT,
)
from mosheh.types.basic import (
    Annotation,
    Args,
    AssertionMessage,
    AssertionTest,
    CodeSnippet,
    CodebaseDict,
    Decorator,
    Docstring,
    FilePath,
    ImportedIdentifier,
    Inheritance,
    Kwargs,
    ModuleName,
    ModulePath,
    StandardReturn,
    Token,
    Value,
)
from mosheh.types.enums import (
    FileRole,
    FunctionType,
    ImportType,
    Statement,
)
from mosheh.utils import build_nav_struct, indent_code


logger: Logger = getLogger('mosheh')


def process_codebase(
    codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]],
    root: str,
    exit: str,
    basedir: str = '',
    codebase_nav_path: str = 'Codebase',
) -> None:
    """
    Recursively processes a codebase and generates documentation for each file.

    This function traverses a codebase structure, processes each file's statements
    and generates corresponding Markdown documentation. The documentation is written
    to the specified output directory. If some file contains nested dictionaries,
    the function recursively processes each nested level.

    Key concepts:
    - Recursive Processing: Handles both individual and nested dirs and files.
    - File Documentation: Converts statements into documentation and writes to a common
        standardized structure.
    - Directory Structure: Preserves directory structure in the output documentation.

    Example:

    ```python
    process_codebase(codebase, '/root', '/output')
    # Processes the codebase and generates documentation in the '/output' directory.
    ```

    :param codebase: The codebase to process, which can contain files or nested dirs.
    :type codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]]
    :param root: The root directory of the project.
    :type root: str
    :param exit: The output directory where documentation will be saved.
    :type exit: str
    :param basedir: The base directory used during the recursive traversal.
    :type basedir: str = ''
    :param codebase_nav_path: Expected codebase nav name to be used/found.
    :type codebase_nav_path: str = 'Codebase'
    :return: None
    :rtype: None
    """

    parents: list[str] = list(codebase.keys())
    docs_path: FilePath = path.join(exit, 'docs')

    for key in parents:
        value = codebase[key]
        new_path: str = path.join(basedir, key)

        if isinstance(value, list):
            logger.debug(f"\tEvaluating file '{key}' of {parents}")
            _process_file(
                key,
                value,
                new_path,
                root,
                docs_path,
                codebase_nav_path=codebase_nav_path,
            )
        else:
            logger.debug(f"\tReprocessing dir '{key}' of {parents}")
            process_codebase(value, root, exit, new_path)


def _process_file(
    key: str,
    stmts: list[StandardReturn],
    file_path: FilePath,
    root: str,
    docs_path: FilePath,
    codebase_nav_path: str = 'Codebase',
) -> None:
    """
    Processes a file's stmts and generates it's corresponding documentation.

    Converts a list of stmts into a Markdown document, writes the content to
    the appropriate file path, and updates the navigation structure for the
    documentation. If the necessary folder path does not exist, it is created.

    Key concepts:
    - Statement Processing: Converts stmts into Markdown format.
    - File Writing: Saves the generated content to the appropriate file.
    - Navigation Update: Updates the documentation's navigation structure.

    Example:

    ```python
    _process_file('module_name', stmts, 'src/module.py', '/root', '/docs')
    # Processes the stmts from 'module.py' and generates corresponding markdown docs.
    ```

    :param key: The key representing the module or file being processed.
    :type key: str
    :param stmts: The list of stmts that represent the code to be documented.
    :type stmts: list[StandardReturn]
    :param file_path: The path to the source file, used to derive output locations.
    :type file_path: str
    :param root: The root directory of the project.
    :type root: str
    :param docs_path: The path to the documentation directory.
    :type docs_path: str
    :param codebase_nav_path: Expected codebase nav name to be used/found.
    :type codebase_nav_path: str = 'Codebase'
    :return: None
    :rtype: None
    """

    if not stmts:
        logger.debug(f'\t\t{key} empty, has no statement')
        return

    content: str = _codebase_to_markdown(stmts, file_path)
    output_file_path: FilePath = path.join(
        docs_path, codebase_nav_path, file_path.removeprefix(root) + '.md'
    )
    folder_path: FilePath = path.dirname(output_file_path)

    if not path.exists(path.join('.', folder_path)):
        makedirs(path.join('.', folder_path))
        logger.debug(f'\t\tCreated path "{folder_path}"')

    _write_to_file(output_file_path, content)


def _codebase_to_markdown(file_data: list[StandardReturn], basedir: str) -> str:
    """
    Converts a file's processed data into a structured Markdown representation.

    This function processes a list of stmts extracted from a Python file and
    generates a Markdown-formatted string. It categorizes stmts into imports,
    constants, classes, functions, and assertions, ensuring that each type is
    documented appropriately. If a category has no stmts, a default informational
    message is added.

    Key concepts:
    - Statement Handling: The function processes different types of stmts
        (imports, assignments, class and function definitions, etc.) and organizes
        them into corresponding sections.
    - Markdown Generation: The output is formatted using a predefined Markdown
        template (`FILE_MARKDOWN`) that structures the documentation by category.
    - Category Defaults: If no stmts exist for a particular category, an
        informational block is added to indicate it's absence.

    Example:

    ```python
    file_data: list[StandardReturn] = [
        {'statement': Statement.Import, 'name': 'os', ...},
        {'statement': Statement.ClassDef, 'name': 'MyClass', ...},
    ]
    _codebase_to_markdown(file_data, '/path/to/module/file.py')
    # Outputs a Markdown string with sections for imports and classes
    ```

    :param file_data: A list of statement dict for the parsed contents of a Python file.
    :type file_data: list[StandardReturn]
    :param basedir: The file in-process' base dir, used to generate the module path.
    :type basedir: str
    :return: A Markdown-formatted string documenting the contents of the file.
    :rtype: str
    """

    __meta__: StandardReturn = file_data.pop(0)

    filename: str = basedir.split(path.sep)[-1]
    role: str = cast(FileRole, __meta__.get('__role__')).value
    file_path: str = (
        basedir.removesuffix(filename)
        .replace(path.sep, '.')
        .removeprefix('..')
        .removeprefix('.')
        .removesuffix('.')
    )
    filedoc: str = cast(str, __meta__.get('__docstring__'))
    imports: str = ''
    constants: str = ''
    classes: str = ''
    functions: str = ''
    assertions: str = ''

    logger.debug(f'\t\t\tFile: {basedir}')
    for stmt in file_data:
        match stmt['statement']:
            case Statement.Import:
                imports += _handle_import(stmt)

            case Statement.ImportFrom:
                imports += _handle_import_from(stmt)

            case Statement.Assign:
                constants += _handle_assign(stmt)

            case Statement.AnnAssign:
                constants += _handle_annassign(stmt)

            case Statement.ClassDef:
                classes += _handle_class_def(stmt)

            case Statement.FunctionDef | Statement.AsyncFunctionDef:
                functions += _handle_function_def(stmt)

            case Statement.Assert:
                assertions += _handle_assert(stmt)

            case _:
                logger.error(
                    f'Statement shoud not be processed here: {stmt["statement"]}'
                )

    if not imports:
        logger.debug('\t\t\tNo imports defined here')
        imports = '!!! info "NO IMPORT DEFINED HERE"'
    if not constants:
        logger.debug('\t\t\tNo constants defined here')
        constants = '!!! info "NO CONSTANT DEFINED HERE"'
    if not classes:
        logger.debug('\t\t\tNo classes defined here')
        classes = '!!! info "NO CLASS DEFINED HERE"'
    if not functions:
        logger.debug('\t\t\tNo functions defined here')
        functions = '!!! info "NO FUNCTION DEFINED HERE"'
    if not assertions:
        logger.debug('\t\t\tNo assertions defined here')
        assertions = '!!! info "NO ASSERT DEFINED HERE"'

    return FILE_MARKDOWN.format(
        filename=filename,
        role=role,
        file_path=file_path,
        filedoc=filedoc,
        imports=imports,
        constants=constants,
        classes=classes,
        functions=functions,
        assertions=assertions,
    )


def _write_to_file(file_path: FilePath, content: str) -> None:
    """
    Writes content to a specified file.

    This function opens a file at the given path in write mode and writes the provided
    content to it. The content is written using UTF-8 encoding, ensuring compatibility
    with various char sets.

    Key concepts:
    - File Writing: Opens a file for writing and writes the content.
    - UTF-8 Encoding: Ensures the file is written with UTF-8 for proper char handling.

    Example:

    ```python
    _write_to_file('output.md', 'This is some content.')
    # Writes the content "This is some content." to 'output.md'.
    ```

    :param file_path: The path to the file where the content will be written.
    :type file_path: FilePath
    :param content: The content to be written to the file.
    :type content: str
    :return: None
    :rtype: None
    """

    with open(path.join('.', file_path), 'w', encoding='utf-8') as file:
        file.write(content)
        logger.debug(f'\t\t\tContent written to "{file_path.split(sep)[-1]}"')


def _handle_import(stmt: StandardReturn) -> str:
    """
    Generates a Markdown representation for an `import` statement.

    This function processes an `import ...` statement from a parsed Python file,
    formatting it into a structured Markdown block. The output includes the import
    name, category and the indented code snippet.

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
    handle_import(stmt)
    # Outputs a formatted Markdown string representing the import
    ```

    :param stmt: A dict containing the details of the import statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the import statement.
    :rtype: str
    """

    name: ModuleName = cast(ModuleName, stmt['name'])
    category: ImportType = cast(ImportType, stmt['category'])
    code: CodeSnippet = indent_code(cast(CodeSnippet, stmt['code']))

    return IMPORT_MD_STRUCT.format(
        name=name,
        _path=None,
        category=category.value,
        code=code,
    )


def _handle_import_from(stmt: StandardReturn) -> str:
    """
    Generates a Markdown representation for an `import` statement.

    This function processes a `from ... import ...` statement from a parsed Python
    file, formatting it into a structured Markdown block. The output includes the
    import name, category and the indented code snippet.

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
    handle_import(stmt)
    # Outputs a formatted Markdown string representing the import
    ```

    :param stmt: A dict containing the details of the import statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the import statement.
    :rtype: str
    """

    name: ImportedIdentifier = cast(ImportedIdentifier, stmt['name'])
    _path: ModulePath = cast(ModulePath, stmt['path'])
    category: ImportType = cast(ImportType, stmt['category'])
    code: CodeSnippet = indent_code(f'from {_path} import {name}')

    return IMPORT_MD_STRUCT.format(
        name=name,
        _path=_path,
        category=category.value,
        code=code,
    )


def _handle_assign(stmt: StandardReturn) -> str:
    """
    Generates a Markdown representation for an `assign` statement.

    This function processes a `token = value` statement from a parsed Python file,
    formatting it into a structured Markdown block. The output includes the assign
    tokens, value and the indented code snippet.

    Key concepts:
    - Assign Handling: Extracts the assign statement's details (tokens, value, code)
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
    handle_assign(stmt)
    # Outputs a formatted Markdown string representing the assign
    ```

    :param stmt: A dict containing the details of the assign statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the assign statement.
    :rtype: str
    """

    tokens: Token = ', '.join(cast(list[Token], stmt['tokens']))
    value: Value = cast(Value, stmt['value'])
    code: CodeSnippet = indent_code(cast(str, stmt['code']))

    return ASSIGN_MD_STRUCT.format(
        token=tokens,
        _type='Unknown',
        value=value,
        code=code,
    )


def _handle_annassign(stmt: StandardReturn) -> str:
    """
    Generates a Markdown representation for an `annotated assign` statement.

    This function processes a `token: type = value` statement from a parsed Python file,
    formatting into a structured Markdown block. The output includes the assign name,
    annotation, value and the indented code snippet.

    Key concepts:
    - Annotated Assign Handling: Extracts the assign statement's details (name, annot,
        value, code) and formats them for documentation.
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
    handle_annassign(stmt)
    # Outputs a formatted Markdown string representing the annotated assign
    ```

    :param stmt: A dict containing the details of the annassign statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the annassign statement.
    :rtype: str
    """

    name: Token = cast(Token, stmt['name'])
    annot: Annotation = cast(Annotation, stmt['annot'])
    value: Value = cast(Value, stmt['value'])
    code: CodeSnippet = indent_code(cast(str, stmt['code']))

    return ASSIGN_MD_STRUCT.format(
        token=name,
        _type=annot,
        value=value,
        code=code,
    )


def _handle_class_def(stmt: StandardReturn) -> str:
    """
    Generates a Markdown representation for a `class` definition statement.

    This function processes a class definition from a parsed Python codebase,
    extracting key details such as the class name, inheritance, decorators,
    keyword arguments and the code itself. It formats this information into
    a structured Markdown block for documentation purposes.

    Key concepts:
    - Class Handling: Extracts information about the class, including its name,
        inheritance hierarchy and decorators.
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
        'code': '@dataclass\\nclass MyClass(BaseClass): ...',
    }
    handle_class_def(stmt)
    # Outputs a formatted Markdown string representing the class definition
    ```

    :param stmt: A dict containing the details of the class definition statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the class definition.
    :rtype: str
    """

    name: Token = cast(Token, stmt['name'])
    inheritance: Inheritance = ', '.join(cast(list[Inheritance], stmt['inheritance']))
    decorators: Decorator = (
        ', '.join(cast(list[Decorator], stmt['decorators'])) or 'None'
    )
    kwargs: Kwargs = cast(Kwargs, stmt['kwargs'])
    code: CodeSnippet = indent_code(cast(str, stmt['code']))

    if docstring := cast(Docstring | None, stmt['docstring']):
        docstring = indent_code(docstring)
    else:
        docstring = indent_code('No docstring provided.')

    if not inheritance:
        inheritance = 'None'

    if not kwargs:
        kwargs = 'None'

    return CLASS_DEF_MD_STRUCT.format(
        name=name,
        docstring=docstring,
        inheritance=inheritance,
        decorators=decorators,
        kwargs=kwargs,
        code=code,
    )


def _handle_function_def(stmt: StandardReturn) -> str:
    """
    Generates a Markdown representation for a function definition statement.

    This function processes a function or method definition from a parsed Python
    codebase, extracting details such as the function name, decorators, arguments,
    keyword arguments, return type and the code itself. It formats this information
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
        'decorators': [''],
        'args': 'x: int, y: int',
        'kwargs': '',
        'rtype': 'int',
        'code': 'def sum_thing(x: int, y: int) -> int: return x + y',
    }
    handle_function_def(stmt)
    # Outputs a formatted Markdown string representing the function definition
    ```

    :param stmt: A dict containing the details of the function definition statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the function definition.
    :rtype: str
    """

    name: Token = cast(Token, stmt['name'])
    decorators: Decorator = (
        ', '.join(cast(list[Decorator], stmt['decorators'])) or 'None'
    )
    category: FunctionType = cast(FunctionType, stmt['category'])
    rtype: Annotation = cast(Annotation, stmt['rtype']) or 'Unknown'
    code: CodeSnippet = indent_code(cast(str, stmt['code']))

    if docstring := cast(Docstring | None, stmt['docstring']):
        docstring = indent_code(
            docstring.replace(':param', '\n:param')
            .replace(':type', '\n:type')
            .replace(':return', '\n:return')
            .replace(':rtype', '\n:rtype')
        )
    else:
        docstring = indent_code('No docstring provided.')

    if not (args := cast(Args, stmt['args'])):
        args = 'None'
    if not (kwargs := cast(Kwargs, stmt['kwargs'])):
        kwargs = 'None'

    return FUNCTION_DEF_MD_STRUCT.format(
        name=name,
        docstring=docstring,
        decorators=decorators,
        category=category.value,
        args=args,
        kwargs=kwargs,
        rtype=rtype,
        code=code,
    )


def _handle_assert(stmt: StandardReturn) -> str:
    """
    Generates a Markdown representation for an `assert` statement.

    This function processes a `assert x` statement from a parsed Python codebase,
    extracting the test condition, optional message and the code itself. It formats
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
    handle_assert(stmt)
    # Outputs a formatted Markdown string representing the assert statement
    ```

    :param stmt: A dictionary containing the details of the assert statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the assert statement.
    :rtype: str
    """

    test: AssertionTest = cast(AssertionTest, stmt['test'])
    msg: AssertionMessage = cast(AssertionMessage, stmt['msg'])
    code: CodeSnippet = indent_code(cast(str, stmt['code']))

    return ASSERT_MD_STRUCT.format(test=test, msg=msg, code=code)


def get_update_set_nav(
    mkdocs_yml: FilePath,
    cleaned_codebase: CodebaseDict,
    codebase_nav_path: str = 'Codebase',
) -> None:
    """
    Sets the `mkdocs.yml` Nav "Codebase" section to the current state, updating it.

    Reading the current `mkdocs.yml` file, loads and parses it's data, extracts the
    "Nav" section and search for the Expected Codebase Nav path, defaulting to
    `'Codebase'`; after this, if success, updates the nav list with the new codebase
    data and, finally, saves this changes dumping the file updating just the codebase
    section.

    :param mkdocs_yml: Ready-to-use "mkdocs.yml" path.
    :type mkdocs_yml: FilePath
    :param codebase: Dict containing nodes representing `.py` files and their stmts.
    :type codebase: CodebaseDict
    :param codebase_nav_path: Expected codebase nav name to be used/found.
    :type codebase_nav_path: str = 'Codebase'
    :return: None
    :rtype: None
    """

    with open(mkdocs_yml, encoding='utf-8') as f:
        yml: dict[str, list[Any]] = yaml.load(f.read(), Loader=yaml.CLoader)

        try:
            nav_section_index: int = list(list(i.keys())[0] for i in yml['nav']).index(
                codebase_nav_path
            )
        except ValueError:
            logger.error(f'Nav section "{codebase_nav_path}" not found')
            exit()

    yml['nav'][nav_section_index] = {
        codebase_nav_path: build_nav_struct(cleaned_codebase, codebase_nav_path)
    }

    with open(mkdocs_yml, 'w', encoding='utf-8') as f:
        f.write(yaml.dump(yml, Dumper=yaml.CDumper, sort_keys=False, indent=2))


def write_homepage(output_path: FilePath, readme_path: FilePath) -> None:
    """
    Reads the content of a given README file path and writes to the doc homepage.

    As simple as can be, just add some MkDocs lines to remove (hide) both ToC and
    navigation, so the page has nothing on the sides, giving more space for the
    main content.

    :param output_path: String for the documentation output.
    :type output_path: FilePath
    :param readme_path: String for the README file.
    :type readme_path: FilePath
    :return: None
    :rtype: None
    """

    homepage: str = path.join(output_path, 'docs', 'index.md')

    with open(readme_path, encoding='utf-8') as f:
        content: list[str] = f.readlines()

    with open(homepage, 'w', encoding='utf-8') as f:
        readme_to_write: list[str] = [
            '---\n',
            'hide:\n',
            '  - navigation\n',
            '  - toc\n',
            '---\n',
            '\n',
            '<br>\n',
            '\n',
        ] + content
        f.writelines(readme_to_write)

    logger.info('"README.md" copied to documentation')
