from hypothesis import given as g
from hypothesis import strategies as st

from mosheh.types.jsoncfg import IOJSON, DefaultJSON, DocumentationJSON


@g(
    st.characters(),
    st.characters(),
    st.characters(),
    st.characters(),
    st.characters(),
    st.characters() | st.none(),
    st.characters() | st.none(),
    st.characters(),
)
def test_documentation_json_typeddict(
    name: str,
    repo: str,
    repo_url: str,
    site_url: str,
    edit_uri: str,
    logo_path: str | None,
    readme_path: str | None,
    codebase_nav_path: str,
) -> None:
    cfg: DocumentationJSON = DocumentationJSON(
        projectName=name,
        repoName=repo,
        repoUrl=repo_url,
        siteUrl=site_url,
        editUri=edit_uri,
        logoPath=logo_path,
        readmePath=readme_path,
        codebaseNavPath=codebase_nav_path,
    )

    expected: dict[str, str | None] = {
        'projectName': name,
        'repoName': repo,
        'repoUrl': repo_url,
        'siteUrl': site_url,
        'editUri': edit_uri,
        'logoPath': logo_path,
        'readmePath': readme_path,
        'codebaseNavPath': codebase_nav_path,
    }

    assert cfg == expected


@g(st.characters(), st.characters())
def test_io_json_typeddict(root_dir: str, output_dir: str) -> None:
    cfg: IOJSON = IOJSON(rootDir=root_dir, outputDir=output_dir)

    expected: dict[str, str] = {'rootDir': root_dir, 'outputDir': output_dir}

    assert cfg == expected


@g(
    st.characters(),
    st.characters(),
    st.characters(),
    st.characters(),
    st.characters(),
    st.characters() | st.none(),
    st.characters() | st.none(),
    st.characters(),
    st.characters(),
    st.characters(),
)
def test_default_json_typeddict(
    name: str,
    repo: str,
    repo_url: str,
    site_url: str,
    edit_uri: str,
    logo_path: str | None,
    readme_path: str | None,
    codebase_nav_path: str,
    root_dir: str,
    output_dir: str,
) -> None:
    doc_cfg: DocumentationJSON = DocumentationJSON(
        projectName=name,
        repoName=repo,
        repoUrl=repo_url,
        siteUrl=site_url,
        editUri=edit_uri,
        logoPath=logo_path,
        readmePath=readme_path,
        codebaseNavPath=codebase_nav_path,
    )

    io_cfg: IOJSON = IOJSON(rootDir=root_dir, outputDir=output_dir)

    cfg: DefaultJSON = DefaultJSON(documentation=doc_cfg, io=io_cfg)

    doc_expected: dict[str, str | None] = {
        'projectName': name,
        'repoName': repo,
        'repoUrl': repo_url,
        'siteUrl': site_url,
        'editUri': edit_uri,
        'logoPath': logo_path,
        'readmePath': readme_path,
        'codebaseNavPath': codebase_nav_path,
    }

    io_expected: dict[str, str] = {'rootDir': root_dir, 'outputDir': output_dir}

    expected: dict[str, dict[str, str] | dict[str, str | None]] = {
        'documentation': doc_expected,
        'io': io_expected,
    }

    assert cfg == expected
