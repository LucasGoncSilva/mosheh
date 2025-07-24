from mosheh.types.jsoncfg import IOJSON, DefaultJSON, DocumentationJSON


def test_documentation_json_typeddict() -> None:
    cfg: DocumentationJSON = DocumentationJSON(
        projectName='Name',
        repoName='repo',
        repoUrl='https://google.com',
        editUri='edit/uri',
        logoPath=None,
        readmePath=None,
    )

    expected: dict[str, str | None] = {
        'projectName': 'Name',
        'repoName': 'repo',
        'repoUrl': 'https://google.com',
        'editUri': 'edit/uri',
        'logoPath': None,
        'readmePath': None,
    }

    assert cfg == expected


def test_io_json_typeddict() -> None:
    cfg: IOJSON = IOJSON(rootDir='.', outputDir='.')

    expected: dict[str, str] = {'rootDir': '.', 'outputDir': '.'}

    assert cfg == expected


def test_default_json_typeddict() -> None:
    doc_cfg: DocumentationJSON = DocumentationJSON(
        projectName='Name',
        repoName='repo',
        repoUrl='https://google.com',
        editUri='edit/uri',
        logoPath=None,
        readmePath=None,
    )

    io_cfg: IOJSON = IOJSON(rootDir='.', outputDir='.')

    cfg: DefaultJSON = DefaultJSON(documentation=doc_cfg, io=io_cfg)

    doc_expected: dict[str, str | None] = {
        'projectName': 'Name',
        'repoName': 'repo',
        'repoUrl': 'https://google.com',
        'editUri': 'edit/uri',
        'logoPath': None,
        'readmePath': None,
    }

    io_expected: dict[str, str] = {'rootDir': '.', 'outputDir': '.'}

    expected: dict[str, dict[str, str] | dict[str, str | None]] = {
        'documentation': doc_expected,
        'io': io_expected,
    }

    assert cfg == expected
