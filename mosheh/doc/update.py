"""
Used to update the Nav and optionally the homepage of a documentation site,
this file handles the `types.basic.CodebaseDict` and rewrites the `mkdocs.yml`
Nav structure based on its contents.

The only existing function here is `update_doc`, which encapsulates all
underlying logic and utility calls.

There’s logic for safely cleaning the codebase, rebuilding the navigation tree,
modifying the YAML structure, and copying over the README to serve as homepage,
all using internal calls for functions such as `process_codebase` and
`get_update_set_nav`.
"""

from logging import Logger, getLogger
from os import path

from mosheh.doc.shared import process_codebase,get_update_set_nav
from mosheh.types.basic import CodebaseDict, FilePath
from mosheh.utils import remove_abspath_from_codebase


logger: Logger = getLogger('mosheh')


def update_doc(
    *,
    codebase: CodebaseDict,
    root: str,
    output: str,
    readme_path: str | None,
    codebase_nav_path: str = 'Codebase',
) -> None:
    """
    Updates an existing documentation for a Python codebase using MkDocs.

    This function updates a MkDocs project at the specified output path, rewrites a
    configuration file and processes the provided codebase to generate documentation.

    Key concepts:
    - Kwargs: By starting args with "*", this function only accepts key-word arguments.
    - MkDocs: A static site generator that's geared towards project documentation.
    - Codebase Processing: The function relies on `process_codebase` to handle the
      codebase structure and populate the documentation content based on Python files
      and their stmts.
    - Configuration: Rebuilds a `mkdocs.yml` Nav config file with new project details.
    - Homepage: If `readme_path` is provided, so the `index.md` file provided by MkDocs
      is overwriten by the `README.md` found at provided `readme_path` file.

    :param codebase: Dict containing nodes representing `.py` files and their stmts.
    :type codebase: CodebaseDict
    :param root: Root dir, where the analysis starts.
    :type root: str
    :param output: Path for documentation output, where to be created.
    :type output: str
    :param readme_path: The path of the `README.md` file, to be used as homepage.
    :type readme_path: str | None
    :param codebase_nav_path: Expected codebase nav name to be used/found.
    :type codebase_nav_path: str = 'Codebase'
    :return: None
    :rtype: None
    """

    clean_codebase: CodebaseDict = remove_abspath_from_codebase(codebase)
    output_path: str = path.abspath(output)
    mkdocs_yml: FilePath = path.join(output_path, 'mkdocs.yml')

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
