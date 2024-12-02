
# File: `main.py`
Path: `mosheh`



---

## Imports

### `#!py import ArgumentParser`

Path: `#!py argparse`

Category: Native

??? example "SNIPPET"

    ```py
    from argparse import ArgumentParser
    ```

### `#!py import Namespace`

Path: `#!py argparse`

Category: Native

??? example "SNIPPET"

    ```py
    from argparse import Namespace
    ```

### `#!py import RawDescriptionHelpFormatter`

Path: `#!py argparse`

Category: Native

??? example "SNIPPET"

    ```py
    from argparse import RawDescriptionHelpFormatter
    ```

### `#!py import path`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import path
    ```

### `#!py import read_codebase`

Path: `#!py codebase`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from codebase import read_codebase
    ```

### `#!py import CodebaseDict`

Path: `#!py custom_types`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from custom_types import CodebaseDict
    ```

### `#!py import generate_doc`

Path: `#!py doc`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from doc import generate_doc
    ```



---

## Consts

### `#!py ROOT`

Type: `#!py str`

Value: `#!py args.root`

??? example "SNIPPET"

    ```py
    ROOT: str = args.root
    ```

### `#!py PROJ_NAME`

Type: `#!py str`

Value: `#!py path.abspath(path.curdir).split(path.sep)[-1].upper()`

??? example "SNIPPET"

    ```py
    PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
    ```

### `#!py REPO_NAME`

Type: `#!py str`

Value: `#!py args.repo_name`

??? example "SNIPPET"

    ```py
    REPO_NAME: str = args.repo_name
    ```

### `#!py REPO_URL`

Type: `#!py str`

Value: `#!py args.repo_url`

??? example "SNIPPET"

    ```py
    REPO_URL: str = args.repo_url
    ```

### `#!py LOGO_PATH`

Type: `#!py str`

Value: `#!py args.logo_path`

??? example "SNIPPET"

    ```py
    LOGO_PATH: str = args.logo_path
    ```

### `#!py README_PATH`

Type: `#!py str`

Value: `#!py args.readme_path`

??? example "SNIPPET"

    ```py
    README_PATH: str = args.readme_path
    ```

### `#!py EXIT`

Type: `#!py str`

Value: `#!py args.exit`

??? example "SNIPPET"

    ```py
    EXIT: str = args.exit
    ```



---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def main`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def main() -> None:
        """
        This is the script's entrypoint, kinda where everything starts.

        It takes no parameters inside code itself, but uses ArgumentParser to deal with
        them. Parsing the args, extracts the infos provided to deal and construct the
        output doc based on them.

        :rtype: None
        """
        parser: ArgumentParser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-root', type=str, help='Root dir, where the analysis starts.', required=True)
        parser.add_argument('--repo-name', type=str, default='GitHub', help='Name of the code repository to be mapped.')
        parser.add_argument('--repo-url', type=str, default='https://github.com/', help='URL of the code repository to be mapped.')
        parser.add_argument('--logo-path', type=str, default='', help='Path for documentation/project logo in .svg | .png format.')
        parser.add_argument('--readme-path', type=str, default='', help='Path for README.md file to replace as homepage.')
        parser.add_argument('--exit', type=str, default='.', help='Path for documentation output, where to be created.')
        args: Namespace = parser.parse_args()
        ROOT: str = args.root
        PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
        REPO_NAME: str = args.repo_name
        REPO_URL: str = args.repo_url
        LOGO_PATH: str = args.logo_path
        README_PATH: str = args.readme_path
        EXIT: str = args.exit
        data: CodebaseDict = read_codebase(ROOT)
        generate_doc(codebase=data, root=ROOT, exit=EXIT, proj_name=PROJ_NAME, edit_uri='', repo_name=REPO_NAME, repo_url=REPO_URL, logo_path=LOGO_PATH, readme_path=README_PATH)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
