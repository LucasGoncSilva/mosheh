#!/usr/bin/env python

"""
Mosheh, a tool for documenting projects, from Python to Python.

Basically, Mosheh lists all files you points to, saves every single notorious statement
of definition on each file iterated, all using Python `ast` native module for handling
the AST and then generating (using MkDocs) a documentation respecting the dirs and files
hierarchy.

The stuff documented for each file is avaible at https://lucasgoncsilva.github.io/mosheh
"""

__author__ = 'LucasGonc'
__maintainer__ = 'LucasGonc'
__credits__ = ['LucasGonc']
__email__ = 'lucasgoncsilva04@gmail.com'

__license__ = 'MIT'
__repository__ = 'https://github.com/LucasGoncSilva/mosheh'
__keywords__ = ['CLI', 'Python', 'documentation', 'MkDocs', 'automation', 'generation']

__version__ = '1.3.4'
__date__ = '2025-01-07'
__status__ = 'Production'

__copyright__ = 'Copyright (c) 2025 Lucas Gonçalves da Silva'

__description__ = __doc__


from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, basicConfig, getLogger

from rich.logging import RichHandler

from mosheh.commands import init, run


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
        - 3: Info (default)
        - 4: Debug
    :type v: int
    :return: None.
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
    subparsers = parser.add_subparsers(required=True)

    parser_init = subparsers.add_parser(
        'init', help='Create the config file for using Mosheh.'
    )
    parser_init.add_argument(
        '--path', type=str, default='.', help='Where the config file must be.'
    )
    parser_init.set_defaults(func=init)

    parser_run = subparsers.add_parser('run', help='Actually runs the program itself.')
    parser_run.add_argument(
        '--json', type=str, default='./', help='Where the config file must be.'
    )
    parser_run.set_defaults(func=run)

    parser.add_argument(
        '--verbose',
        type=int,
        default=3,
        choices=(0, 1, 2, 3, 4),
        help='Verbosity level, from 0 (quiet/critical) to 4 (overshare/debug).',
    )

    args: Namespace = parser.parse_args()

    set_logging_config(args.verbose)

    logger = getLogger('mosheh')
    logger.info('Logger config done')

    args.func(args)


if __name__ == '__main__':
    main()
