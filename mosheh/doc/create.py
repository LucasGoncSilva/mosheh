"""
Used to create the output documentation, this file deals with the codebase generated
`types.basic.CodebaseDict` and creates `.md` files based on its contained information.

The only public/exposed function here is `create_doc`, which takes care of all of the
private functions.

There’s logic for safely cleaning the codebase, rebuilding the navigation tree,
modifying the YAML structure, and copying over the README to serve as homepage,
all using internal calls for functions such as `process_codebase` and
`get_update_set_nav`.
"""

import subprocess
from logging import Logger, getLogger
from os import makedirs, path
from shutil import copy2

from mosheh.constants import DEFAULT_MKDOCS_YML
from mosheh.doc.shared import get_update_set_nav, process_codebase
from mosheh.types.basic import CodebaseDict, FilePath
from mosheh.utils import remove_abspath_from_codebase


logger: Logger = getLogger('mosheh')


def create_doc(
    *,
    codebase: CodebaseDict,
    root: str,
    output: str,
    proj_name: str,
    logo_path: str | None,
    readme_path: str | None,
    edit_uri: str = 'blob/main/documentation/docs',
    repo_name: str = 'GitHub',
    repo_url: str = 'https://github.com',
    codebase_nav_path: str = 'Codebase',
) -> None:
    """
    Generates a documentation for a Python codebase using MkDocs.

    This function creates a new MkDocs project at the specified output path, writes a
    configuration file and processes the provided codebase to generate documentation.

    Key concepts:
    - Kwargs: By starting args with "*", this function only accepts key-word arguments.
    - MkDocs: A static site generator that's geared towards project documentation.
    - Codebase Processing: The function relies on `_process_codebase` to handle the
      codebase structure and populate the documentation content based on Python files
      and their stmts.
    - Configuration: Builds a `mkdocs.yml` configuration file with project details,
      including repository information and editing URI.
    - Homepage: If `readme_path` is provided, so the `index.md` file provided by MkDocs
      is overwriten by the `README.md` found at provided `readme_path` file.

    :param codebase: Dict containing nodes representing `.py` files and their stmts.
    :type codebase: CodebaseDict
    :param root: Root dir, where the analysis starts.
    :type root: str
    :param output: Path for documentation output, where to be created.
    :type output: str
    :param proj_name: The name of the project, for generating MkDocs configuration.
    :type proj_name: str
    :param logo_path: Path for doc/project logo, same Material MkDocs's formats.
    :type logo_path: str | None
    :param readme_path: The path of the `README.md` file, to be used as homepage.
    :type readme_path: str | None
    :param edit_uri: URI to view raw or edit blob file, default is
                        `'blob/main/documentation/docs'`.
    :type edit_uri: str
    :param repo_name: Name of the code repository to be mapped, default is `'GitHub'`.
    :type repo_name: str
    :param repo_url: The URL of the repository, used for linking in the documentation.
    :type repo_url: str
    :param codebase_nav_path: Expected codebase nav name to be used/found.
    :type codebase_nav_path: str = 'Codebase'
    :return: None
    :rtype: None
    """

    clean_codebase: CodebaseDict = remove_abspath_from_codebase(codebase)
    output_path: str = path.abspath(output)
    mkdocs_yml: str = path.join(output_path, 'mkdocs.yml')

    try:
        logger.info('Running MkDocs project')
        result = subprocess.run(
            ['mkdocs', 'new', output_path],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.debug(f'\t{result.stdout}' or '\tNo MkDocs output')
        logger.info('MkDocs project created')
    except subprocess.CalledProcessError as e:
        logger.error(f'Error: {e.stderr}')
        raise e

    logger.info('Creating default "mkdocs.yml"')
    _create_default_mkdocs(
        mkdocs_yml,
        output,
        proj_name,
        logo_path,
        edit_uri,
        repo_name,
        repo_url,
        codebase_nav_path,
    )
    logger.info('Default "mkdocs.yml" created')

    logger.info('Processing codebase')
    process_codebase(clean_codebase, root, output, codebase_nav_path=codebase_nav_path)
    logger.info('Codebase processed successfully')

    logger.info('Getting and updating Nav')
    get_update_set_nav(mkdocs_yml, clean_codebase, codebase_nav_path)
    logger.debug('\tNav addeded to mkdocs.yml')

    if readme_path:
        homepage: str = path.join(output_path, 'docs', 'index.md')

        with open(readme_path, encoding='utf-8') as f:
            content: list[str] = f.readlines()

        with open(homepage, 'w', encoding='utf-8') as f:
            f.writelines(content)

        logger.info('\t"README.md" copied to documentation')


def _create_default_mkdocs(
    mkdocs_yml: FilePath,
    output: str,
    proj_name: str,
    logo_path: str | None,
    edit_uri: str = 'blob/main/documentation/docs',
    repo_name: str = 'GitHub',
    repo_url: str = 'https://github.com',
    codebase_nav_path: str = 'Codebase',
) -> None:
    with open(mkdocs_yml, 'w', encoding='utf-8') as f:
        f.write(
            _default_doc_config(
                proj_name=proj_name,
                output=output,
                logo_path=logo_path,
                edit_uri=edit_uri,
                repo_name=repo_name,
                repo_url=repo_url,
                codebase_nav_path=codebase_nav_path,
            )
        )


def _default_doc_config(
    *,
    proj_name: str,
    output: str,
    logo_path: str | None,
    edit_uri: str = 'blob/main/documentation/docs',
    repo_name: str = 'GitHub',
    repo_url: str = 'https://github.com/',
    codebase_nav_path: str = 'Codebase',
) -> str:
    """
    Generates the default configuration for an MkDocs documentation project.

    This function creates an `mkdocs.yml` configuration file with project details,
    repository information, and an optional logo. If a logo is provided, it is copied
    to the documentation's image directory.

    Key features:
    - Supports setting project and repository information.
    - Handles optional logos and ensures they are placed in the correct directory.
    - Returns a formatted YAML configuration as a string.

    :param proj_name: The name of the project, for generating MkDocs configuration.
    :type proj_name: str
    :param output: Path for documentation output, where to be created.
    :type output: str
    :param logo_path: Path for doc/project logo, same Material MkDocs's formats.
    :type logo_path: str | None
    :param edit_uri: URI to view raw or edit blob file, default is
                        `'blob/main/documentation/docs'`.
    :type edit_uri: str
    :param repo_name: Name of the code repository to be mapped, default is `'GitHub'`.
    :type repo_name: str
    :param repo_url: The URL of the repository, used for linking in the documentation.
    :type repo_url: str
    :return: Formatted MkDocs YAML configuration.
    :rtype: str
    """

    new_logo_path: str

    if logo_path:
        extension: str = path.splitext(logo_path)[-1]
        logo_file_path: str = path.join(output, 'docs', 'img')
        file_name: str = path.join(logo_file_path, f'logo{extension}')
        logger.debug('Logo path handling done')

        if not path.exists(logo_file_path):
            makedirs(logo_file_path)
            logger.debug(f'{logo_file_path} logo file path created')

        copy2(logo_path, file_name)
        logger.info(f'{logo_path} copied to {file_name}')

        new_logo_path = file_name.removeprefix(path.join(output, 'docs', ''))

    else:
        new_logo_path = 'https://squidfunk.github.io/mkdocs-material/assets/favicon.png'

    return DEFAULT_MKDOCS_YML.format(
        proj_name=proj_name,
        edit_uri=edit_uri,
        repo_name=repo_name,
        repo_url=repo_url,
        logo_path=new_logo_path,
        codebase_nav_path=codebase_nav_path,
    )
