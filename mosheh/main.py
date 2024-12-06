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

__author__ = 'LucasGonc'
__copyright__ = 'Copyright (c) 2024 Lucas Gonçalves da Silva'
__credits__ = ['Lucas Silva']
__license__ = 'MIT'
__maintainer__ = 'LucasGonc'
__email__ = 'lucasgoncsilva04@gmail.com'
__repository__ = 'https://github.com/LucasGoncSilva/mosheh'
__description__ = __doc__
__keywords__ = ['CLI', 'documentation', 'doc']
__version__ = '1.1.0'
__date__ = '2024-12-06'
__status__ = 'Production'


from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from os import path

from .codebase import read_codebase
from .custom_types import CodebaseDict
from .doc import generate_doc


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
        '--output',
        type=str,
        default='.',
        help='Path for documentation output, where to be created.',
    )

    # Arguments Parsing
    args: Namespace = parser.parse_args()

    ROOT: str = args.root
    PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
    REPO_NAME: str = args.repo_name
    REPO_URL: str = args.repo_url
    EDIT_URI: str = args.edit_uri
    LOGO_PATH: str | None = args.logo_path
    README_PATH: str | None = args.readme_path
    OUTPUT: str = args.output

    # Codebase Reading
    data: CodebaseDict = read_codebase(ROOT)

    # Doc Generation
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


if __name__ == '__main__':
    main()
