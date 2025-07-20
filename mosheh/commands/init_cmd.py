"""
Encapsulating the `init` command logic, this file uses the `types.jsoncfg` TypedDict
classes for ensure the correct structure over the `mosheh.json` config file generated.
"""

from argparse import Namespace
from json import dumps
from logging import Logger, getLogger
from os.path import abspath, join
from typing import Final

from mosheh.types.jsoncfg import IOJSON, DefaultJSON, DocumentationJSON


logger: Logger = getLogger('mosheh')


DOCUMENTATION_JSON: Final[DocumentationJSON] = DocumentationJSON(
    projectName='Mosheh',
    repoName='mosheh',
    repoUrl='https://github.com/lucasgoncsilva/mosheh',
    editUri='blob/main/documentation/docs',
    logoPath='./path/to/logo.svg',
    readmePath='./path/to/README.md',
    codebaseNavPath='Codebase',
)


IO_JSON: Final[IOJSON] = IOJSON(
    rootDir='./app/',
    outputDir='./path/to/output/',
)


DEFAULT_JSON: Final[DefaultJSON] = {
    'documentation': DOCUMENTATION_JSON,
    'io': IO_JSON,
}


def init(args: Namespace) -> None:
    """
    Creates the `mosheh.json` config file.

    By using the `types.jsoncfg` TypedDict classes for ensure the correct structure
    over the `mosheh.json` config file generated, this function incorporates the role
    of bringing this config file, following the path designited by the own CLI call.

    :param args: Namespace object containing the creation information.
    :type args: argparse.Namespace
    :return: None
    :rtype: None
    """

    try:
        file_path: str = join(args.path, 'mosheh.json')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(dumps(DEFAULT_JSON, indent=2))

        logger.info(f'"mosheh.json" created at {abspath(file_path)}')
        logger.debug(f'"mosheh.json" = {DEFAULT_JSON}')

    except FileNotFoundError:
        logger.error(f'"{args.path}" does not exists as directory')
    except PermissionError:
        logger.error(
            '"--path" must be a valid dir and Mosheh must have permission for this,'
            f' got "{args.path}" instead'
        )
    except Exception as e:
        logger.critical(f'Not implemented logic for {type(e).__name__}: {e}')
