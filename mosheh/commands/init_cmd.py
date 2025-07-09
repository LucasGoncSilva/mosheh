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
    try:
        filepath: str = join(args.path, 'mosheh.json')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(dumps(DEFAULT_JSON, indent=2))

        logger.info(f'"mosheh.json" created at {abspath(filepath)}')
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
