from typing import Any
from unittest.mock import MagicMock, mock_open, patch

from mosheh.doc import generate_doc
from mosheh.types.basic import CodebaseDict
from mosheh.types.enums import Statement


def side_effect_join(*args: Any) -> str:
    return '/'.join(args)


def side_effect_abspath(dirpath: str) -> str:
    return f'/mocked/abs/{dirpath}'


@patch('subprocess.run')
@patch('builtins.open', new_callable=mock_open)
@patch('os.path.abspath')
@patch('os.path.join')
@patch('mosheh.doc._process_codebase')
@patch('mosheh.doc._default_doc_config')
def test_generate_doc(
    mock_default_doc_config: MagicMock,
    mock_process_codebase: MagicMock,
    mock_path_join: MagicMock,
    mock_path_abspath: MagicMock,
    mock_open: MagicMock,
    mock_subprocess_run: MagicMock,
) -> None:
    mock_default_doc_config.return_value = 'mocked_mkdocs_config'
    mock_path_abspath.side_effect = side_effect_abspath
    mock_path_join.side_effect = side_effect_join
    mock_subprocess_run.return_value = MagicMock(stdout='')

    codebase: CodebaseDict = {
        'some_file.py': [
            {
                'statement': Statement.FunctionDef,
                'name': 'sum_thing',
                'decorators': ['@staticmethod'],
                'args': 'x: int, y: int',
                'kwargs': None,
                'rtype': 'int',
                'code': 'def sum_thing(x: int, y: int) -> int: return x + y',
            }
        ]
    }
    root: str = '/project/root'
    output: str = '/output/path'
    proj_name: str = 'Test Project'
    logo_path: str | None = '/path/to/logo.png'
    readme_path: str | None = '/path/to/README.md'
    edit_uri: str = 'blob/main/docs'
    repo_name: str = 'GitHub'
    repo_url: str = 'https://github.com'

    generate_doc(
        codebase=codebase,
        root=root,
        output=output,
        proj_name=proj_name,
        logo_path=logo_path,
        readme_path=readme_path,
        edit_uri=edit_uri,
        repo_name=repo_name,
        repo_url=repo_url,
    )

    mock_subprocess_run.assert_called_once_with(
        ['mkdocs', 'new', '/mocked/abs//output/path'],
        check=True,
        capture_output=True,
        text=True,
    )

    mock_default_doc_config.assert_called_once_with(
        proj_name=proj_name,
        output=output,
        logo_path=logo_path,
        edit_uri=edit_uri,
        repo_name=repo_name,
        repo_url=repo_url,
    )

    mock_process_codebase.assert_called_once_with(codebase, root, output)

    mock_open.assert_any_call(
        '/mocked/abs//output/path/mkdocs.yml', 'w', encoding='utf-8'
    )

    if readme_path:
        mock_open.assert_any_call(readme_path, encoding='utf-8')
        mock_open.assert_any_call(
            '/mocked/abs//output/path/docs/index.md', 'w', encoding='utf-8'
        )
