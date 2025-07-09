from typing import TypedDict


class DocumentationJSON(TypedDict):
    projectName: str
    repoName: str
    repoUrl: str
    editUri: str
    logoPath: str | None
    readmePath: str | None


class IOJSON(TypedDict):
    rootDir: str
    outputDir: str


class DefaultJSON(TypedDict):
    documentation: DocumentationJSON
    io: IOJSON
