#!/usr/bin/env python

"""
Mosheh, automatic and elegant documentation of Python code with MkDocs.

Inspirated by `cargodoc` - a Rust tool for code documenting - and using MkDocs +
Material MkDocs, Mosheh is an **easy, fast, plug-and-play** tool which saves time
while **automating** the process of documenting the **source code of a Python
codebase**.

The stuff documented for each file is avaible at https://lucasgoncsilva.github.io/mosheh
"""


from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, basicConfig, getLogger

from rich.logging import RichHandler

from mosheh.commands import create, init, update


def set_logging_config(v: int = 3) -> None:
    """
    Configures the logging level for the application based on the provided verbosity.

    Logging is handled using `RichHandler` for enhanced terminal output. The verbosity
    level `v` controls the logging granularity for the `mosheh` logger, and optionally
    for the `mkdocs` logger in debug mode.

    :param v: Verbosity level, from 0 (critical) to 4 (debug). Defaults to 3 (info).\n
        - 0: Critical
        - 1: Error
        - 2: Warning
        - 3: Info (default)
        - 4: Debug
    :type v: int = 3
    :return: None
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

    :return: None
    :rtype: None
    """

    # Parser Creation
    parser: ArgumentParser = ArgumentParser(
        description=(__doc__),
        formatter_class=RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(required=True)

    # Command: init
    parser_init = subparsers.add_parser(
        'init', help='Creates the config file for using Mosheh.'
    )
    parser_init.add_argument(
        '--path', type=str, default='.', help='Path for `mosheh.json` config file.'
    )
    parser_init.set_defaults(func=init)

    # Command: create
    parser_create = subparsers.add_parser(
        'create', help='Creates the final documentation based on `mosheh.json`.'
    )
    parser_create.add_argument(
        '--json', type=str, default='.', help='Path for `mosheh.json` config file.'
    )
    parser_create.set_defaults(func=create)

    # Command: update
    parser_update = subparsers.add_parser(
        'update',
        help='Updates existing documentation "nav.Codebase" based on `mosheh.json`'
        " and reading the current codebase's situation.",
    )
    parser_update.add_argument(
        '--json', type=str, default='.', help='Path for `mosheh.json` config file.'
    )
    parser_update.set_defaults(func=update)

    parser.add_argument(
        '--verbose',
        type=int,
        default=3,
        choices=(0, 1, 2, 3, 4),
        help='Verbosity level, from 0 (quiet/critical) to 4 (overshare/debug).',
    )

    args: Namespace = parser.parse_args()

    set_logging_config(args.verbose)

    args.func(args)


if __name__ == '__main__':
    main()
