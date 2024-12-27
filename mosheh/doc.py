import subprocess
from logging import Logger, getLogger
from os import makedirs, path
from shutil import copy2
from typing import cast

from .constants import (
    ASSERT_MD_STRUCT,
    ASSIGN_MD_STRUCT,
    CLASS_DEF_MD_STRUCT,
    DEFAULT_MKDOCS_YML,
    FILE_MARKDOWN,
    FUNCTION_DEF_MD_STRUCT,
    IMPORT_MD_STRUCT,
)
from .custom_types import (
    CodebaseDict,
    FileRole,
    FunctionType,
    ImportType,
    StandardReturn,
    Statement,
)
from .utils import indent_code


logger: Logger = getLogger('mosheh')


NAV_DIRS: list[str] = []
NAV_MD: list[str] = ['nav:\n  - Homepage: index.md\n']


def generate_doc(
    *,
    codebase: CodebaseDict,
    root: str,
    output: str,
    proj_name: str,
    logo_path: str | None,
    readme_path: str | None,
    edit_uri: str = 'blob/main/documentation/docs',
    repo_name: str = 'GitHub',
    repo_url: str = 'https://github.com',
) -> None:
    """
    Generates a documentation structure for a Python codebase using MkDocs.

    This function creates a new MkDocs project at the specified output path, writes a
    configuration file, and processes the provided codebase to generate documentation.

    Key concepts:
    - Kwargs: By starting args with "*", this function only accepts key-word arguments.
    - MkDocs: A static site generator that's geared towards project documentation.
    - Codebase Processing: The function relies on `process_codebase` to handle the
      codebase structure and populate the documentation content based on Python files
      and their stmts.
    - Configuration: Builds a `mkdocs.yml` configuration file with project details,
      including repository information and editing URI.
    - Homepage: If `readme_path` is provided, so the `index.md` file provided by MkDocs
      is overwriten by the `README.md` found at provided `readme_path` file.

    :param codebase: Dict containing nodes representing `.py` files and their stmts.
    :type codebase: CodebaseDict
    :param root: Root dir, where the analysis starts.
    :type root: str
    :param output: Path for documentation output, where to be created.
    :type output: str
    :param proj_name: The name of the project, for generating MkDocs configuration.
    :type proj_name: str
    :param logo_path: Path for doc/project logo, same Material MkDocs's formats.
    :type logo_path: str | None
    :param readme_path: The path of the `README.md` file, to be used as homepage.
    :type readme_path: str | None
    :param edit_uri: URI to view raw or edit blob file, default is
                        `'blob/main/documentation/docs'`.
    :type edit_uri: str
    :param repo_name: Name of the code repository to be mapped, default is `'GitHub'`.
    :type repo_name: str
    :param repo_url: The URL of the repository, used for linking in the documentation.
    :type repo_url: str
    :return: Nothing, just generates documentation files in the specified output path.
    :rtype: None
    """

    output_path: str = path.abspath(output)
    mkdocs_yml: str = path.join(output_path, 'mkdocs.yml')

    try:
        logger.debug('Running MkDocs')
        result = subprocess.run(
            ['mkdocs', 'new', output_path],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.debug(result.stdout)
        logger.info('MkDocs created')
    except subprocess.CalledProcessError as e:
        logger.critical(f'Error: {e.stderr}')
        raise e

    logger.info('Creating default mkdocs.yml')
    with open(mkdocs_yml, 'w', encoding='utf-8') as f:
        f.write(
            _default_doc_config(
                proj_name=proj_name,
                output=output,
                logo_path=logo_path,
                edit_uri=edit_uri,
                repo_name=repo_name,
                repo_url=repo_url,
            )
        )

    logger.info('Processing codebase')
    _process_codebase(codebase, root, output)

    with open(mkdocs_yml, 'a', encoding='utf-8') as f:
        f.writelines(NAV_MD)
        logger.debug('Nav added to mkdocs.yml')

    if readme_path is not None:
        homepage: str = path.join(output_path, 'docs', 'index.md')

        with open(readme_path, encoding='utf-8') as f:
            logger.debug(f'{readme_path} read')
            content: list[str] = f.readlines()

        with open(homepage, 'w', encoding='utf-8') as f:
            logger.debug(f'{homepage} written')
            f.writelines(content)

        logger.info('README.md copied to documentation')


def _default_doc_config(
    *,
    proj_name: str,
    output: str,
    logo_path: str | None,
    edit_uri: str = 'blob/main/documentation/docs',
    repo_name: str = 'GitHub',
    repo_url: str = 'https://github.com/',
) -> str:
    """
    Generates the default configuration for an MkDocs documentation project.

    This function creates an `mkdocs.yml` configuration file with project details,
    repository information, and an optional logo. If a logo is provided, it is copied
    to the documentation's image directory.

    Key features:
    - Supports setting project and repository information.
    - Handles optional logos and ensures they are placed in the correct directory.
    - Returns a formatted YAML configuration as a string.

    :param proj_name: The name of the project, for generating MkDocs configuration.
    :type proj_name: str
    :param output: Path for documentation output, where to be created.
    :type output: str
    :param logo_path: Path for doc/project logo, same Material MkDocs's formats.
    :type logo_path: str
    :param edit_uri: URI to view raw or edit blob file, default is
                        `'blob/main/documentation/docs'`.
    :type edit_uri: str
    :param repo_name: Name of the code repository to be mapped, default is `'GitHub'`.
    :type repo_name: str
    :param repo_url: The URL of the repository, used for linking in the documentation.
    :type repo_url: str
    :return: Formatted MkDocs YAML configuration.
    :rtype: str
    """

    if logo_path is not None:
        ext: str = path.splitext(logo_path)[-1]
        logo_file_path: str = path.join(output, 'docs', 'img')
        file_name: str = path.join(logo_file_path, f'logo{ext}')
        logger.debug('Logo path handling done')

        if not path.exists(logo_file_path):
            makedirs(logo_file_path)
            logger.debug(f'{logo_file_path} logo file path created')

        copy2(logo_path, file_name)
        logger.info(f'{logo_path} copied to {file_name}')

        logo_path = file_name.removeprefix(path.join(output, 'docs', ''))

    else:
        logo_path = 'https://squidfunk.github.io/mkdocs-material/assets/favicon.png'

    return DEFAULT_MKDOCS_YML.format(
        proj_name=proj_name,
        edit_uri=edit_uri,
        repo_name=repo_name,
        repo_url=repo_url,
        logo_path=logo_path,
    )


def _codebase_to_markdown(filedata: list[StandardReturn], basedir: str) -> str:
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
      informational block is added to indicate its absence.

    Example:
    ```python
    filedata: list[StandardReturn] = [
        {'statement': Statement.Import, 'name': 'os', ...},
        {'statement': Statement.ClassDef, 'name': 'MyClass', ...},
    ]
    _codebase_to_markdown(filedata, '/path/to/module/file.py')
    # Outputs a Markdown string with sections for imports and classes
    ```

    :param filedata: A list of statement dict for the parsed contents of a Python file.
    :type filedata: list[StandardReturn]
    :param basedir: The file in-process' base dir, used to generate the module path.
    :type basedir: str
    :return: A Markdown-formatted string documenting the contents of the file.
    :rtype: str
    """

    filename: str = basedir.split(path.sep)[-1]
    role: str = cast(FileRole, filedata.pop(0).get('__role__')).value
    filepath: str = (
        basedir.removesuffix(filename).replace(path.sep, '.').removesuffix('.')
    )
    filedoc: str = ''
    imports: str = ''
    constants: str = ''
    classes: str = ''
    functions: str = ''
    assertions: str = ''

    logger.debug(f'File: {basedir}')
    for stmt in filedata:
        match stmt['statement']:
            case Statement.Import:
                imports += _handle_import(stmt)
                logger.debug(f'\tStatement: {stmt}')

            case Statement.ImportFrom:
                imports += _handle_import_from(stmt)
                logger.debug(f'\tStatement: {stmt}')

            case Statement.Assign:
                constants += _handle_assign(stmt)
                logger.debug(f'\tStatement: {stmt}')

            case Statement.AnnAssign:
                constants += _handle_annassign(stmt)
                logger.debug(f'\tStatement: {stmt}')

            case Statement.ClassDef:
                classes += _handle_class_def(stmt)
                logger.debug(f'\tStatement: {stmt}')

            case Statement.FunctionDef | Statement.AsyncFunctionDef:
                functions += _handle_function_def(stmt)
                logger.debug(f'\tStatement: {stmt}')

            case Statement.Assert:
                assertions += _handle_assert(stmt)
                logger.debug(f'\tStatement: {stmt}')

            case _:
                logger.error('Statement shoud not be processed here:')
                logger.error(stmt['statement'])

    if not len(imports):
        logger.debug('No imports defined here')
        imports = '!!! info "NO IMPORT DEFINED HERE"'
    if not len(constants):
        logger.debug('No constants defined here')
        constants = '!!! info "NO CONSTANT DEFINED HERE"'
    if not len(classes):
        logger.debug('No classes defined here')
        classes = '!!! info "NO CLASS DEFINED HERE"'
    if not len(functions):
        logger.debug('No functions defined here')
        functions = '!!! info "NO FUNCTION DEFINED HERE"'
    if not len(assertions):
        logger.debug('No assertions defined here')
        assertions = '!!! info "NO ASSERT DEFINED HERE"'

    return FILE_MARKDOWN.format(
        filename=filename,
        role=role,
        filepath=filepath,
        filedoc=filedoc,
        imports=imports,
        constants=constants,
        classes=classes,
        functions=functions,
        assertions=assertions,
    )


def _handle_import(stmt: StandardReturn) -> str:
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
    handle_import(stmt)
    # Outputs a formatted Markdown string representing the import
    ```

    :param stmt: A dict containing the details of the import statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the import statement.
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


def _handle_import_from(stmt: StandardReturn) -> str:
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
    handle_import(stmt)
    # Outputs a formatted Markdown string representing the import
    ```

    :param stmt: A dict containing the details of the import statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the import statement.
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


def _handle_assign(stmt: StandardReturn) -> str:
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
    handle_assign(stmt)
    # Outputs a formatted Markdown string representing the assign
    ```

    :param stmt: A dict containing the details of the assign statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the assign statement.
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


def _handle_annassign(stmt: StandardReturn) -> str:
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
    handle_annassign(stmt)
    # Outputs a formatted Markdown string representing the annotated assign
    ```

    :param stmt: A dict containing the details of the annassign statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the annassign statement.
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


def _handle_class_def(stmt: StandardReturn) -> str:
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
    handle_class_def(stmt)
    # Outputs a formatted Markdown string representing the class definition
    ```

    :param stmt: A dict containing the details of the class definition statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the class definition.
    :rtype: str
    """

    name: str = cast(str, stmt['name'])
    docstring: str | None = cast(str | None, stmt['docstring'])
    inherit: str = ', '.join(cast(list[str], stmt['inheritance']))
    decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
    kwargs: str = cast(str, stmt['kwargs'])
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    if not docstring:
        docstring = 'No `docstring` provided.'

    if not kwargs:
        kwargs = 'None'

    return CLASS_DEF_MD_STRUCT.format(
        name=name,
        docstring=docstring,
        inherit=inherit,
        decorators=decorators,
        kwargs=kwargs,
        code=code,
    )


def _handle_function_def(stmt: StandardReturn) -> str:
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
    handle_function_def(stmt)
    # Outputs a formatted Markdown string representing the function definition
    ```

    :param stmt: A dict containing the details of the function definition statement.
    :type stmt: StandardReturn
    :return: A formatted Markdown string documenting the function definition.
    :rtype: str
    """

    name: str = cast(str, stmt['name'])
    decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
    category: str = cast(FunctionType, stmt['category']).value
    docstring: str | None = cast(str | None, stmt['docstring'])
    args: str = cast(str, stmt['args'])
    kwargs: str = cast(str, stmt['kwargs'])
    rtype: str = cast(str, stmt['rtype']) or 'Unknown'
    _code: str = cast(str, stmt['code'])
    code: str = indent_code(_code)

    if not docstring:
        docstring = 'No `docstring` provided.'
    if docstring:
        docstring = (
            docstring.replace(':param', '\n:param')
            .replace(':type', '\n:type')
            .replace(':return', '\n:return')
            .replace(':rtype', '\n:rtype')
        )

    if not args:
        args = 'None'
    if not kwargs:
        kwargs = 'None'

    return FUNCTION_DEF_MD_STRUCT.format(
        name=name,
        docstring=docstring,
        decorators=decorators,
        category=category,
        args=args,
        kwargs=kwargs,
        rtype=rtype,
        code=code,
    )


def _handle_assert(stmt: StandardReturn) -> str:
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
    handle_assert(stmt)
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


def _process_codebase(
    codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]],
    root: str,
    exit: str,
    basedir: str = '',
) -> None:
    """
    Recursively processes a codebase and generates documentation for each file.

    This function traverses a codebase structure, processes each file's statements,
    and generates corresponding Markdown documentation. The documentation is written
    to the specified output directory. If the codebase contains nested dictionaries,
    the function recursively processes each nested level.

    Key concepts:
    - Recursive Processing: Handles both individual files and nested dirs.
    - File Documentation: Converts statements into documentation and writes to output.
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
    :type basedir: str
    :return: None.
    :rtype: None
    """

    parents: list[str] = list(codebase.keys())
    docs_path: str = path.join(exit, 'docs')
    logger.debug('"parents: list[str]" and "docs_path: str" defined')

    for key in parents:
        logger.debug(f'Evaluating {key} of {parents}')
        value = codebase[key]
        new_path: str = path.join(basedir, key)

        if isinstance(value, list):
            logger.debug(f'Processing file {key}')
            _process_file(key, value, new_path, root, docs_path)
        else:
            _process_codebase(value, root, exit, new_path)


def _process_file(
    key: str,
    stmts: list[StandardReturn],
    file_path: str,
    root: str,
    docs_path: str,
) -> None:
    """
    Processes a file's stmts and generates corresponding documentation.

    This function converts a list of stmts into a Markdown document, writes
    the content to the appropriate file path, and updates the navigation structure
    for the documentation. If the necessary folder path does not exist, it is created.

    Key concepts:
    - Statement Processing: Converts stmts into Markdown format.
    - File Writing: Saves the generated content to the appropriate file.
    - Navigation Update: Updates the documentation's navigation structure.

    Example:
    ```python
    __process_file('module_name', stmts, 'src/module.py', '/root', '/docs')
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
    :return: None.
    :rtype: None
    """

    if not stmts:
        logger.debug(f'{key} empty, has no statement')
        return

    content: str = _codebase_to_markdown(stmts, file_path)
    output_file_path: str = path.join(
        docs_path, 'Codebase', file_path.removeprefix(root) + '.md'
    )
    folder_path: str = path.dirname(output_file_path)

    if not path.exists(folder_path):
        makedirs(folder_path)
        logger.debug(f'{folder_path} created')

    __write_to_file(output_file_path, content)
    __update_navigation(folder_path, docs_path, key, output_file_path)


def __write_to_file(file_path: str, content: str) -> None:
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
    __write_to_file('output.md', 'This is some content.')
    # Writes the content "This is some content." to 'output.md'.
    ```

    :param file_path: The path to the file where the content will be written.
    :type file_path: str
    :param content: The content to be written to the file.
    :type content: str
    :return: None.
    :rtype: None
    """

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
        logger.debug(f'Content written to {file_path}')


def __update_navigation(
    folder_path: str, docs_path: str, key: str, output_file_path: str
) -> None:
    """
    Updates the navigation structure for documentation generation.

    This function builds and updates a nested navigation structure for documentation
    files based on the provided folder path and file location. It ensures that
    each segment of the path is represented in the navigation hierarchy, maintaining
    the correct indentation levels.

    Key concepts:
    - Navigation Hierarchy: Constructs a structured navigation tree from folder paths.
    - Indentation: Adjusts indentation dynamically based on folder depth.
    - Path Normalization: Handles path manipulation to generate correct relative paths.

    Example:
    ```python
    __update_navigation(
        'project/docs/module',
        'project/docs',
        'functions',
        'project/docs/module/functions.md',
    )
    # Updates the global NAV_DIRS and NAV_MD structs with the right navigation entries.
    ```

    :param folder_path: The full path to the folder containing the documentation files.
    :type folder_path: str
    :param docs_path: The root path to the documentation directory.
    :type docs_path: str
    :param key: The label or name for the current documentation entry.
    :type key: str
    :param output_file_path: The path to the output documentation file.
    :type output_file_path: str
    :return: None.
    :rtype: None
    """

    nav_path: list[str] = [
        segment
        for segment in folder_path.removeprefix(docs_path).split(path.sep)
        if segment
    ]
    logger.debug('"nav_path: list[str]" created')

    if not nav_path:
        md_file_path: str = output_file_path.removeprefix(docs_path + path.sep)
        md_line: str = indent_code(f'- {key}: {md_file_path}', 2)
        NAV_MD.append(f'{md_line}\n')
        logger.debug('"NAV_MD" updated with no "nav_path"')
        return

    for i in range(len(nav_path)):
        sub_nav_path: str = path.sep.join(nav_path[: i + 1])
        if sub_nav_path not in NAV_DIRS:
            NAV_DIRS.append(sub_nav_path)
            md_line: str = indent_code(f'- {nav_path[i]}:', 2 * (i + 1))
            NAV_MD.append(f'{md_line}\n')
            logger.debug('"NAV_MD" updated with path not in "NAV_DIRS"')

        if i + 1 == len(nav_path):
            md_file_path: str = output_file_path.removeprefix(docs_path + path.sep)
            md_line: str = indent_code(f'- {key}: {md_file_path}', 2 * (i + 2))
            NAV_MD.append(f'{md_line}\n')
            logger.debug('"NAV_MD" updated')
