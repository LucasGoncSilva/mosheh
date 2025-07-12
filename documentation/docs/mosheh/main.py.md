# File: `main.py`

Role: Python Source Code

Path: `mosheh`

Mosheh, a tool for documenting projects, from Python to Python.

Basically, Mosheh lists all files you points to, saves every single notorious statement
of definition on each file iterated, all using Python `ast` native module for handling
the AST and then generating (using MkDocs) a documentation respecting the dirs and files
hierarchy. The stuff documented for each file is shown below:

- Imports `[ast.Import | ast.ImportFrom]`

  - [x] Type `[Native | TrdParty | Local]`
  - [x] Path (e.g. 'django.http')
  - [x] Code

- Constants `[ast.Assign | ast.AnnAssign]`

  - [x] Name (token name)
  - [x] Typing Annotation (datatype)
  - [x] Value (literal or call)
  - [x] Code

- Classes `[ast.ClassDef]`

  - [x] Description (docstring)
  - [x] Name (class name)
  - [x] Parents (inheritance)
  - [ ] Methods Defined (nums and names)
  - [ ] Example (usage)
  - [x] Code

- Funcs `[ast.FunctionDef | ast.AsyncFunctionDef]`

  - [x] Description (docstring)
  - [x] Name (func name)
  - [x] Type `[Func | Method | Generator | Coroutine]`
  - [x] Parameters (name, type, default)
  - [x] Return Type (datatype)
  - [ ] Raises (exception throw)
  - [ ] Example (usage)
  - [x] Code

- Assertions `[ast.Assert]`

  - [x] Test (assertion by itself)
  - [x] Message (opt. message in fail case)
  - [x] Code

---

## Imports

### `#!py import *`

Path: `#!py metadata`

Category: Local

??? example "Snippet"

    ```py
    from metadata import *
    ```

### `#!py import ArgumentParser`

Path: `#!py argparse`

Category: Native

??? example "Snippet"

    ```py
    from argparse import ArgumentParser
    ```

### `#!py import Namespace`

Path: `#!py argparse`

Category: Native

??? example "Snippet"

    ```py
    from argparse import Namespace
    ```

### `#!py import RawDescriptionHelpFormatter`

Path: `#!py argparse`

Category: Native

??? example "Snippet"

    ```py
    from argparse import RawDescriptionHelpFormatter
    ```

### `#!py import CRITICAL`

Path: `#!py logging`

Category: Native

??? example "Snippet"

    ```py
    from logging import CRITICAL
    ```

### `#!py import DEBUG`

Path: `#!py logging`

Category: Native

??? example "Snippet"

    ```py
    from logging import DEBUG
    ```

### `#!py import ERROR`

Path: `#!py logging`

Category: Native

??? example "Snippet"

    ```py
    from logging import ERROR
    ```

### `#!py import INFO`

Path: `#!py logging`

Category: Native

??? example "Snippet"

    ```py
    from logging import INFO
    ```

### `#!py import WARNING`

Path: `#!py logging`

Category: Native

??? example "Snippet"

    ```py
    from logging import WARNING
    ```

### `#!py import basicConfig`

Path: `#!py logging`

Category: Native

??? example "Snippet"

    ```py
    from logging import basicConfig
    ```

### `#!py import getLogger`

Path: `#!py logging`

Category: Native

??? example "Snippet"

    ```py
    from logging import getLogger
    ```

### `#!py import path`

Path: `#!py os`

Category: Native

??? example "Snippet"

    ```py
    from os import path
    ```

### `#!py import CalledProcessError`

Path: `#!py subprocess`

Category: Native

??? example "Snippet"

    ```py
    from subprocess import CalledProcessError
    ```

### `#!py import RichHandler`

Path: `#!py rich.logging`

Category: 3rd Party

??? example "Snippet"

    ```py
    from rich.logging import RichHandler
    ```

### `#!py import read_codebase`

Path: `#!py codebase`

Category: Local

??? example "Snippet"

    ```py
    from codebase import read_codebase
    ```

### `#!py import CodebaseDict`

Path: `#!py custom_types`

Category: Local

??? example "Snippet"

    ```py
    from custom_types import CodebaseDict
    ```

### `#!py import generate_doc`

Path: `#!py doc`

Category: Local

??? example "Snippet"

    ```py
    from doc import generate_doc
    ```

---

## Consts

### `#!py ROOT`

Type: `#!py str`

Value: `#!py args.root`

??? example "Snippet"

    ```py
    ROOT: str = args.root
    ```

### `#!py PROJ_NAME`

Type: `#!py str`

Value: `#!py path.abspath(path.curdir).split(path.sep)[-1].upper()`

??? example "Snippet"

    ```py
    PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
    ```

### `#!py REPO_NAME`

Type: `#!py str`

Value: `#!py args.repo_name`

??? example "Snippet"

    ```py
    REPO_NAME: str = args.repo_name
    ```

### `#!py REPO_URL`

Type: `#!py str`

Value: `#!py args.repo_url`

??? example "Snippet"

    ```py
    REPO_URL: str = args.repo_url
    ```

### `#!py EDIT_URI`

Type: `#!py str`

Value: `#!py args.edit_uri`

??? example "Snippet"

    ```py
    EDIT_URI: str = args.edit_uri
    ```

### `#!py LOGO_PATH`

Type: `#!py str | None`

Value: `#!py args.logo_path`

??? example "Snippet"

    ```py
    LOGO_PATH: str | None = args.logo_path
    ```

### `#!py README_PATH`

Type: `#!py str | None`

Value: `#!py args.readme_path`

??? example "Snippet"

    ```py
    README_PATH: str | None = args.readme_path
    ```

### `#!py OUTPUT`

Type: `#!py str`

Value: `#!py args.output`

??? example "Snippet"

    ```py
    OUTPUT: str = args.output
    ```

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def set_logging_config`

Type: `#!py Function`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py v: int`

Kwargs: `#!py None`

Configures the logging level for the application based on the provided verbosity.

Logging is handled using `RichHandler` for enhanced terminal output. The verbosity
level `v` controls the logging granularity for the `mosheh` logger, and optionally
for the `mkdocs` logger in debug mode.

:param v: Verbosity level, from 0 (critical) to 4 (debug). Defaults to 3 (info). - 0: Critical - 1: Error - 2: Warning - 3: Info - 4: Debug

:type v: int

:returns: None.

:rtype: None

??? example "Snippet"

    ```py
    def set_logging_config(v: int=3) -> None:
        """
        Configures the logging level for the application based on the provided verbosity.

        Logging is handled using `RichHandler` for enhanced terminal output. The verbosity
        level `v` controls the logging granularity for the `mosheh` logger, and optionally
        for the `mkdocs` logger in debug mode.

        :param v: Verbosity level, from 0 (critical) to 4 (debug). Defaults to 3 (info).
            - 0: Critical
            - 1: Error
            - 2: Warning
            - 3: Info
            - 4: Debug
        :type v: int
        :returns: None.
        :rtype: None
        """
        basicConfig(format='%(message)s', handlers=[RichHandler()])
        match v:
            case 0:
                getLogger('mosheh').setLevel(CRITICAL)
            case 1:
                getLogger('mosheh').setLevel(ERROR)
            case 2:
                getLogger('mosheh').setLevel(WARNING)
            case 3:
                getLogger('mosheh').setLevel(INFO)
            case 4:
                getLogger('mosheh').setLevel(DEBUG)
            case _:
                getLogger('mosheh').setLevel(INFO)
    ```

### `#!py def main`

Type: `#!py Function`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

This is the script's entrypoint, kinda where everything starts.

It takes no parameters inside code itself, but uses ArgumentParser to deal with
them. Parsing the args, extracts the infos provided to deal and construct the
output doc based on them.

:rtype: None

??? example "Snippet"

    ```py
    def main() -> None:
        """
        This is the script's entrypoint, kinda where everything starts.

        It takes no parameters inside code itself, but uses ArgumentParser to deal with
        them. Parsing the args, extracts the infos provided to deal and construct the
        output doc based on them.

        :rtype: None
        """
        parser: ArgumentParser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-root', type=str, help='Root dir, where the analysis starts.', required=True)
        parser.add_argument('--repo-name', type=str, default='GitHub', help='Name of the code repository to be mapped.')
        parser.add_argument('--repo-url', type=str, default='https://github.com/', help='URL of the code repository to be mapped.')
        parser.add_argument('--edit-uri', type=str, default='blob/main/documentation/docs', help='URI to view/edit raw/blob file.')
        parser.add_argument('--logo-path', type=str, default=None, help='Path for doc/project logo, same Material MkDocs formats.')
        parser.add_argument('--readme-path', type=str, default=None, help='Path for README.md file to replace as homepage.')
        parser.add_argument('--verbose', type=int, default=3, help='Verbosity level, from 0 (quiet/critical) to 4 (overshare/debug).')
        parser.add_argument('--output', type=str, default='.', help='Path for documentation output, where to be created.')
        args: Namespace = parser.parse_args()
        set_logging_config(args.verbose)
        logger = getLogger('mosheh')
        logger.info('Logger config done')
        ROOT: str = args.root
        logger.debug(f'ROOT = {ROOT!r}')
        PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
        logger.debug(f'PROJ_NAME = {PROJ_NAME!r}')
        REPO_NAME: str = args.repo_name
        logger.debug(f'REPO_NAME = {REPO_NAME!r}')
        REPO_URL: str = args.repo_url
        logger.debug(f'REPO_URL = {REPO_URL!r}')
        EDIT_URI: str = args.edit_uri
        logger.debug(f'EDIT_URI = {EDIT_URI!r}')
        LOGO_PATH: str | None = args.logo_path
        logger.debug(f'LOGO_PATH = {LOGO_PATH!r}')
        README_PATH: str | None = args.readme_path
        logger.debug(f'README_PATH = {README_PATH!r}')
        OUTPUT: str = args.output
        logger.debug(f'OUTPUT = {OUTPUT!r}')
        logger.info('Arguments parsed successfully')
        logger.info(f'Starting to read codebase: {ROOT}')
        data: CodebaseDict = read_codebase(ROOT)
        logger.info('Codebase read successfully')
        logger.info('Starting to generate documentation')
        try:
            generate_doc(codebase=data, root=ROOT, proj_name=PROJ_NAME, repo_name=REPO_NAME, repo_url=REPO_URL, edit_uri=EDIT_URI, logo_path=LOGO_PATH, readme_path=README_PATH, output=OUTPUT)
            logger.info('Documentation created successfully')
        except CalledProcessError as e:
            logger.critical(e)
    ```

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
