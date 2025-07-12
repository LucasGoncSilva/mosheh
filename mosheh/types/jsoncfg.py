"""
To ensure the correct type notation of the default config file `mosheh.json` this file
invokes the `typing.TypedDict` powers for leading this mission.

The config JSON itself is divided at 2 parts: Documentation and IO:

    - Documentation: handles the project's data and final documentation configuration
    - IO: handles the input and output infos, such as output path and codebase root

The idea here is to use TypedDict as a typing alias plus contract - kinda.
"""

from typing import TypedDict


class DocumentationJSON(TypedDict):
    """Typed-Dict class to ensure right typing for config file's doc section."""

    projectName: str
    repoName: str
    repoUrl: str
    editUri: str
    logoPath: str | None
    readmePath: str | None


class IOJSON(TypedDict):
    """Typed-Dict class to ensure right typing for config file's IO section."""

    rootDir: str
    outputDir: str


class DefaultJSON(TypedDict):
    """Typed-Dict class to ensure right typing for config file itself."""

    documentation: DocumentationJSON
    io: IOJSON
