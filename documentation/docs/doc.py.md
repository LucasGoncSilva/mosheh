# File: `doc.py`

Path: `mosheh`

---

## Imports

### `#!py import subprocess`

Path: `#!py None`

Category: Native

??? example "SNIPPET"

    ```py
    import subprocess
    ```

### `#!py import makedirs`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import makedirs
    ```

### `#!py import mkdir`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import mkdir
    ```

### `#!py import path`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import path
    ```

### `#!py import copy2`

Path: `#!py shutil`

Category: Native

??? example "SNIPPET"

    ```py
    from shutil import copy2
    ```

### `#!py import stdout`

Path: `#!py sys`

Category: Native

??? example "SNIPPET"

    ```py
    from sys import stdout
    ```

### `#!py import cast`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import cast
    ```

### `#!py import ASSERT_MD_STRUCT`

Path: `#!py constants`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from constants import ASSERT_MD_STRUCT
    ```

### `#!py import ASSIGN_MD_STRUCT`

Path: `#!py constants`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from constants import ASSIGN_MD_STRUCT
    ```

### `#!py import CLASS_DEF_MD_STRUCT`

Path: `#!py constants`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from constants import CLASS_DEF_MD_STRUCT
    ```

### `#!py import DEFAULT_MKDOCS_YML`

Path: `#!py constants`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from constants import DEFAULT_MKDOCS_YML
    ```

### `#!py import FILE_MARKDOWN`

Path: `#!py constants`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from constants import FILE_MARKDOWN
    ```

### `#!py import FUNCTION_DEF_MD_STRUCT`

Path: `#!py constants`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from constants import FUNCTION_DEF_MD_STRUCT
    ```

### `#!py import IMPORT_MD_STRUCT`

Path: `#!py constants`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from constants import IMPORT_MD_STRUCT
    ```

### `#!py import CodebaseDict`

Path: `#!py custom_types`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from custom_types import CodebaseDict
    ```

### `#!py import ImportType`

Path: `#!py custom_types`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from custom_types import ImportType
    ```

### `#!py import StandardReturn`

Path: `#!py custom_types`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from custom_types import StandardReturn
    ```

### `#!py import Statement`

Path: `#!py custom_types`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from custom_types import Statement
    ```

### `#!py import indent_code`

Path: `#!py utils`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from utils import indent_code
    ```

---

## Consts

### `#!py NAV_DIRS`

Type: `#!py list[str]`

Value: `#!py []`

??? example "SNIPPET"

    ```py
    NAV_DIRS: list[str] = []
    ```

### `#!py NAV_MD`

Type: `#!py list[str]`

Value: `#!py ['nav:\n']`

??? example "SNIPPET"

    ```py
    NAV_MD: list[str] = ['nav:\n']
    ```

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def generate_doc`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py codebase: CodebaseDict, root: str, exit: str, proj_name: str, edit_uri: str = '', repo_name: str = 'GitHub', repo_url: str = '', logo_path: str = '', readme_path: str = ''`

??? example "SNIPPET"

    ```py
    def generate_doc(*, codebase: CodebaseDict, root: str, exit: str, proj_name: str, edit_uri: str='', repo_name: str='GitHub', repo_url: str='', logo_path: str='', readme_path: str='') -> None:
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
        :param root: The root path of the source code to be documented.
        :type root: str
        :param exit: The output dir where the documentation will be generated.
        :type exit: str
        :param proj_name: The name of the project, for generating MkDocs configuration.
        :type proj_name: str
        :param edit_uri: optional URI for linking to source file edits (defaults to '').
        :type edit_uri: str, optional
        :param repo_name: The repository provider name (defaults to 'GitHub').
        :type repo_name: str, optional
        :param repo_url: The URL of the repository, used for linking in the documentation.
        :type repo_url: str, optional
        :param logo_path: The path of the logo, to be used as icon and favicon.
        :type logo_path: str, optional
        :param readme_path: The path of the `README.md` file, to be used as homepage.
        :type readme_path: str, optional
        :return: Nothing, just generates documentation files in the specified output path.
        :rtype: None
        """
        exit_path: str = path.abspath(exit)
        mkdocs_yml: str = path.join(exit_path, 'mkdocs.yml')
        try:
            result = subprocess.run(['mkdocs', 'new', exit_path], check=True, capture_output=True, text=True)
            stdout.write(result.stdout)
        except subprocess.CalledProcessError as e:
            stdout.write(f'Error: {e.stderr}')
        with open(mkdocs_yml, 'w', encoding='utf-8') as f:
            f.write(default_doc_config(proj_name=proj_name, edit_uri=edit_uri, exit=exit, repo_name=repo_name, repo_url=repo_url, logo_path=logo_path))
        process_codebase(codebase, root, exit)
        with open(mkdocs_yml, 'a', encoding='utf-8') as f:
            f.writelines(NAV_MD)
        if readme_path:
            homepage: str = path.join(exit_path, 'docs', 'index.md')
            with open(readme_path, encoding='utf-8') as f:
                content: list[str] = f.readlines()
            with open(homepage, 'w', encoding='utf-8') as f:
                f.writelines(content)
    ```

### `#!py def default_doc_config`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py proj_name: str, edit_uri: str, exit: str, repo_name: str = 'GitHub', repo_url: str = 'https://github.com/', logo_path: str = ''`

??? example "SNIPPET"

    ```py
    def default_doc_config(*, proj_name: str, edit_uri: str, exit: str, repo_name: str='GitHub', repo_url: str='https://github.com/', logo_path: str='') -> str:
        """
        Generates the default configuration for an MkDocs documentation project.

        This function creates an `mkdocs.yml` configuration file with project details,
        repository information, and an optional logo. If a logo is provided, it is copied
        to the documentation's image directory.

        Key features:
        - Supports setting project and repository information.
        - Handles optional logos and ensures they are placed in the correct directory.
        - Returns a formatted YAML configuration as a string.

        :param proj_name: Name of the project.
        :type proj_name: str
        :param edit_uri: URI for editing doc file, typically a GitHub or GitLab edit link.
        :type edit_uri: str
        :param exit: Base output directory where documentation will be stored.
        :type exit: str
        :param repo_name: Name of the repository hosting the project, default is 'GitHub'.
        :type repo_name: str, optional
        :param repo_url: URL to the project's repository, default is 'https://github.com/'.
        :type repo_url: str, optional
        :param logo_path: Path to the project logo, optional.
        :type logo_path: str, optional
        :return: Formatted MkDocs YAML configuration.
        :rtype: str
        """
        if logo_path:
            ext: str = path.splitext(logo_path)[-1]
            logo_file_path: str = path.join(exit, 'docs', 'img')
            file_name: str = path.join(logo_file_path, f'logo{ext}')
            if not path.exists(logo_file_path):
                makedirs(logo_file_path)
            copy2(logo_path, file_name)
            logo_path = file_name.removeprefix(path.join(exit, 'docs', ''))
        else:
            logo_path = 'https://squidfunk.github.io/mkdocs-material/assets/favicon.png'
        return DEFAULT_MKDOCS_YML.format(proj_name=proj_name, edit_uri=edit_uri, repo_name=repo_name, repo_url=repo_url, logo_path=logo_path)
    ```

### `#!py def codebase_to_markdown`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py filedata: list[StandardReturn], basedir: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def codebase_to_markdown(filedata: list[StandardReturn], basedir: str) -> str:
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
        markdown_doc: str = codebase_to_markdown(filedata, '/path/to/module/file.py')
        markdown_doc
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
        filepath: str = basedir.removesuffix(filename).replace(path.sep, '.').removesuffix('.')
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
        return FILE_MARKDOWN.format(filename=filename, filepath=filepath, filedoc=filedoc, imports=imports, constants=constants, classes=classes, functions=functions, assertions=assertions)
    ```

### `#!py def handle_import`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py stmt: StandardReturn`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
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
        return IMPORT_MD_STRUCT.format(name=name, _path=_path, category=category, code=code)
    ```

### `#!py def handle_import_from`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py stmt: StandardReturn`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
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

        :param stmt: A dict containing the details of the import statement.
        :type stmt: StandardReturn
        :return: A formatted Markdown string documenting the import statement.
        :rtype: str
        """
        name: str = cast(str, stmt['name'])
        _path: str = cast(str, stmt['path'])
        category: str = cast(ImportType, stmt['category']).value
        code: str = indent_code(f'from {_path} import {name}')
        return IMPORT_MD_STRUCT.format(name=name, _path=_path, category=category, code=code)
    ```

### `#!py def handle_assign`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py stmt: StandardReturn`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
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
        return ASSIGN_MD_STRUCT.format(token=tokens, _type=_type, value=value, code=code)
    ```

### `#!py def handle_annassign`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py stmt: StandardReturn`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
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
        return ASSIGN_MD_STRUCT.format(token=name, _type=annot, value=value, code=code)
    ```

### `#!py def handle_class_def`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py stmt: StandardReturn`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
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

        :param stmt: A dict containing the details of the class definition statement.
        :type stmt: StandardReturn
        :return: A formatted Markdown string documenting the class definition.
        :rtype: str
        """
        name: str = cast(str, stmt['name'])
        inherit: str = ', '.join(cast(list[str], stmt['inheritance']))
        decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
        kwargs: str = cast(str, stmt['kwargs'])
        _code: str = cast(str, stmt['code'])
        code: str = indent_code(_code)
        if not kwargs:
            kwargs = 'None'
        return CLASS_DEF_MD_STRUCT.format(name=name, inherit=inherit, decorators=decorators, kwargs=kwargs, code=code)
    ```

### `#!py def handle_function_def`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py stmt: StandardReturn`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
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

        :param stmt: A dict containing the details of the function definition statement.
        :type stmt: StandardReturn
        :return: A formatted Markdown string documenting the function definition.
        :rtype: str
        """
        name: str = cast(str, stmt['name'])
        decorators: str = ', '.join(cast(list[str], stmt['decorators'])) or 'None'
        args: str = cast(str, stmt['args'])
        kwargs: str = cast(str, stmt['kwargs'])
        rtype: str = cast(str, stmt['rtype']) or 'Unknown'
        _code: str = cast(str, stmt['code'])
        code: str = indent_code(_code)
        if not args:
            args = 'None'
        if not kwargs:
            kwargs = 'None'
        return FUNCTION_DEF_MD_STRUCT.format(name=name, decorators=decorators, args=args, kwargs=kwargs, rtype=rtype, code=code)
    ```

### `#!py def handle_assert`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py stmt: StandardReturn`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
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
    ```

### `#!py def process_codebase`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]], root: str, exit: str, basedir: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def process_codebase(codebase: dict[str, CodebaseDict] | dict[str, list[StandardReturn]], root: str, exit: str, basedir: str='') -> None:
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
        :type basedir: str, optional, default is ''
        :return: None.
        :rtype: None
        """
        parents: list[str] = list(codebase.keys())
        docs_path: str = path.join(exit, 'docs')
        for key in parents:
            value = codebase[key]
            new_path: str = path.join(basedir, key)
            if isinstance(value, list):
                __process_file(key, value, new_path, root, docs_path)
            else:
                process_codebase(value, root, exit, new_path)
    ```

### `#!py def __process_file`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py key: str, stmts: list[StandardReturn], file_path: str, root: str, docs_path: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def __process_file(key: str, stmts: list[StandardReturn], file_path: str, root: str, docs_path: str) -> None:
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
            return
        content: str = codebase_to_markdown(stmts, file_path)
        output_file_path: str = path.join(docs_path, file_path.removeprefix(root) + '.md')
        folder_path: str = path.dirname(output_file_path)
        if not path.exists(folder_path):
            makedirs(folder_path)
        __write_to_file(output_file_path, content)
        __update_navigation(folder_path, docs_path, key, output_file_path)
    ```

### `#!py def __write_to_file`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py file_path: str, content: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
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
    ```

### `#!py def __update_navigation`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py folder_path: str, docs_path: str, key: str, output_file_path: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def __update_navigation(folder_path: str, docs_path: str, key: str, output_file_path: str) -> None:
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
        nav_path: list[str] = [segment for segment in folder_path.removeprefix(docs_path).split(path.sep) if segment]
        nav_path = nav_path or ['Root']
        for i in range(len(nav_path)):
            sub_nav_path: str = path.sep.join(nav_path[:i + 1])
            if sub_nav_path not in NAV_DIRS:
                NAV_DIRS.append(sub_nav_path)
                md_line: str = indent_code(f'- {nav_path[i]}:', 2 * (i + 1))
                NAV_MD.append(f'{md_line}\n')
            if i + 1 == len(nav_path):
                md_file_path: str = output_file_path.removeprefix(docs_path + path.sep)
                md_line: str = indent_code(f'- {key}: {md_file_path}', 2 * (i + 2))
                NAV_MD.append(f'{md_line}\n')
    ```

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
