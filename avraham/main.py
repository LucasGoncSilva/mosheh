#!/usr/bin/env python

"""
Avraham is a script for generating documentations for projects, from Python to Python.

Basically, Avraham lists all files you points to, saves every single notorious statement
of definition on each file iterated, all using Python "ast" native module for handling
the AST and then generating (using MkDocs) a documentation repecting the dirs and files
hierarchy. The stuff documented for each file are listed below:

- Imports: [ast.Import | ast.ImportFrom]
    - Type: Native | 3rd Party | Local
    - Path (e.g. 'django.http')

- Constants: [ast.Assign | ast.AnnAssign]
    - Name (token name)
    - Typing Notation (datatype)
    - Value (literal or call)

- Classes: [ast.ClassDef]
    - Description (docstring)
    - Name (class name)
    - Parents (inheritance)
    - Methods Defined (nums and names)
    - Example (usage)

- Funcs: [ast.FunctionDef | ast.AsyncFunctionDef]
    - Description (docstring)
    - Name (func name)
    - Type: Func | Method | Generator | Coroutine
    - Parameters (name, type, default)
    - Return Type (datatype)
    - Raises (exception throw)
    - Example (usage)

- Assertions: [ast.Assert]
    - Test (assertion by itself)
    - Message (opt. message in fail case)
"""

__author__ = 'Lucas Silva'
__copyright__ = 'Do\' know'
__credits__ = ['Lucas Silva']
__license__ = 'MIT'
__maintainer__ = 'Lucas Silva'
__email__ = 'lucasgoncsilva04@gmail.com'
__repository__ = 'https://github.com/LucasGoncSilva/avraham'
__description__ = __doc__
__keywords__ = ['CLI', 'documentation', 'doc']
__version__ = '0.0.0'
__date__ = '2024-11-19'
__status__ = 'Development'


from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from os import path

from doc import Lang, generate_doc
from python import read_codebase
from custom_types import CodebaseDict


def main() -> None:
    """
    This is the script's entrypoint, kinda where everything starts.

    It takes no parameters inside code itself, but uses ArgumentParser to deal with them.
    Parsing the args, extracts the infos provided to deal and construct the output doc
    based on them.
    """

    parser: ArgumentParser = ArgumentParser(
        description=(__doc__),
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '-root',
        type=str,
        help='root, base dir',
        required=True,
    )
    parser.add_argument(
        '--lang',
        type=str,
        default='en',
        help='lang for doc output',
    )
    parser.add_argument(
        '--repo-name',
        type=str,
        default='GitHub',
        help='repo name',
    )
    parser.add_argument(
        '--repo-url',
        type=str,
        default='https://github.com/',
        help='repo URL',
    )
    parser.add_argument(
        '--exit',
        type=str,
        default='.',
        help='path for doc output',
    )

    args: Namespace = parser.parse_args()

    ROOT: str = args.root
    PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
    REPO_NAME: str = args.repo_name
    REPO_URL: str = args.repo_url
    EXIT: str = args.exit

    LANG: Lang = {'pt-BR': Lang.PT_BR, 'en': Lang.EN}.get(args.lang, Lang.EN)

    data: CodebaseDict = read_codebase(ROOT)

    print(data)

    generate_doc(EXIT, PROJ_NAME, LANG, '', REPO_NAME, REPO_URL)


if __name__ == '__main__':
    main()
