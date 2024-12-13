#!/usr/bin/env python

"""
Mosheh, a tool for creating docs for projects, from Python to Python.

Basically, Mosheh lists all files you points to, saves every single notorious statement
of definition on each file iterated, all using Python `ast` native module for handling
the AST and then generating (using MkDocs) a documentation respecting the dirs and files
hierarchy. The stuff documented for each file are listed below:

- Imports `[ast.Import | ast.ImportFrom]`
  - [x] Type `[Native | TrdParty | Local]`
  - [x] Path (e.g. 'django.http')
  - [x] Code

- Constants `[ast.Assign | ast.AnnAssign]`
  - [x] Name (token name)
  - [x] Typing Notation (datatype)
  - [x] Value (literal or call)
  - [x] Code

- Classes `[ast.ClassDef]`
  - [ ] Description (docstring)
  - [x] Name (class name)
  - [x] Parents (inheritance)
  - [ ] Methods Defined (nums and names)
  - [ ] Example (usage)
  - [x] Code

- Funcs `[ast.FunctionDef | ast.AsyncFunctionDef]`
  - [ ] Description (docstring)
  - [x] Name (func name)
  - [ ] Type `[Func | Method | Generator | Coroutine]`
  - [x] Parameters (name, type, default)
  - [x] Return Type (datatype)
  - [ ] Raises (exception throw)
  - [ ] Example (usage)
  - [x] Code

- Assertions `[ast.Assert]`
  - [x] Test (assertion by itself)
  - [x] Message (opt. message in fail case)
  - [x] Code
"""

from .metadata import *  # noqa: F403


__description__ = __doc__


from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, basicConfig, getLogger
from os import path
from subprocess import CalledProcessError

from rich.logging import RichHandler

from .codebase import read_codebase
from .custom_types import CodebaseDict
from .doc import generate_doc


def set_logging_config(v: int = 3) -> None:
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

    basicConfig(
        format='%(message)s',
        handlers=[RichHandler()],
    )

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


def main() -> None:
    """
    This is the script's entrypoint, kinda where everything starts.

    It takes no parameters inside code itself, but uses ArgumentParser to deal with
    them. Parsing the args, extracts the infos provided to deal and construct the
    output doc based on them.

    :rtype: None
    """

    # Parser Creation
    parser: ArgumentParser = ArgumentParser(
        description=(__doc__),
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '-root',
        type=str,
        help='Root dir, where the analysis starts.',
        required=True,
    )
    parser.add_argument(
        '--repo-name',
        type=str,
        default='GitHub',
        help='Name of the code repository to be mapped.',
    )
    parser.add_argument(
        '--repo-url',
        type=str,
        default='https://github.com/',
        help='URL of the code repository to be mapped.',
    )
    parser.add_argument(
        '--edit-uri',
        type=str,
        default='blob/main/documentation/docs',
        help='URI to view/edit raw/blob file.',
    )
    parser.add_argument(
        '--logo-path',
        type=str,
        default=None,
        help='Path for doc/project logo, same Material MkDocs formats.',
    )
    parser.add_argument(
        '--readme-path',
        type=str,
        default=None,
        help='Path for README.md file to replace as homepage.',
    )
    parser.add_argument(
        '--verbose',
        type=int,
        default=3,
        help='Verbosity level, from 0 (quiet/critical) to 4 (overshare/debug).',
    )
    parser.add_argument(
        '--output',
        type=str,
        default='.',
        help='Path for documentation output, where to be created.',
    )

    # Arguments Parsing
    args: Namespace = parser.parse_args()

    set_logging_config(args.verbose)

    logger = getLogger('mosheh')
    logger.info('Logger config done')

    ROOT: str = args.root
    logger.debug(f'{ROOT = }')

    PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
    logger.debug(f'{PROJ_NAME = }')

    REPO_NAME: str = args.repo_name
    logger.debug(f'{REPO_NAME = }')

    REPO_URL: str = args.repo_url
    logger.debug(f'{REPO_URL = }')

    EDIT_URI: str = args.edit_uri
    logger.debug(f'{EDIT_URI = }')

    LOGO_PATH: str | None = args.logo_path
    logger.debug(f'{LOGO_PATH = }')

    README_PATH: str | None = args.readme_path
    logger.debug(f'{README_PATH = }')

    OUTPUT: str = args.output
    logger.debug(f'{OUTPUT = }')

    logger.info('Arguments parsed successfully')

    # Codebase Reading
    logger.info(f'Starting to read codebase: {ROOT}')
    data: CodebaseDict = read_codebase(ROOT)
    logger.info('Codebase read successfully')

    # Doc Generation
    logger.info('Starting to generate documentation')
    try:
        generate_doc(
            codebase=data,
            root=ROOT,
            proj_name=PROJ_NAME,
            repo_name=REPO_NAME,
            repo_url=REPO_URL,
            edit_uri=EDIT_URI,
            logo_path=LOGO_PATH,
            readme_path=README_PATH,
            output=OUTPUT,
        )
        logger.info('Documentation created successfully')
    except CalledProcessError as e:
        logger.critical(e)


if __name__ == '__main__':
    main()
