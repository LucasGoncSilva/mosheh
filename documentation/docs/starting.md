# Getting Starded

The Homepage already introduced Mosheh's usage in a nutshell and just by readind there you are already able to use it, but here we are going to cover it in details.

## Installation

To install Mosheh there is no secret, you can literally just tell your package manager to install `mosheh` and use it. As it has no production-like role, it's highly recommended to install as dev dependency, also saving as it as well.

### uv

An extremely fast Python package and project manager, [uv](https://docs.astral.sh/uv/) is written in [Rust](https://www.rust-lang.org/) and backed by [Astral](https://astral.sh/), the creators of [Ruff](https://docs.astral.sh/ruff/). In a few words, **uv** has an ambitious proposal: use the power of Rust to replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv` and more dev tools like these. To install Mosheh with **uv** just use the command below:

```sh
uv add mosheh --dev
```

By doing it, **uv** is going to save Mosheh as dev dependency on `pyproject.toml` with the structure below, where `x.x.x` is the last version released or the chosen one:

```yaml hl_lines="5 6"
[project]
name = "your-project"
...

[dependency-groups]
dev = ["mosheh>=x.x.x"]
```

For more information about **uv** installation please check: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

!!! note "Personal Recomendation"

    **uv** is the personal recomendation for managing project dependencies and handling development tasks, such as building; check it out for your personal use case.

### PIP

The most commonly used tool for dependency management, **PIP** is frequently installed with the Python Interpreter. It has no command or parameter to install libs as development dependency, but there is a recommended solution to this: separate a production requirements file from a development one. To achieve this goal follow the steps below:

1. Create a `requirements.dev.txt` or similar: `#!sh touch requirements.dev.txt`
1. Tell it to read main/production `requirements.txt`: `#!sh echo "-r ./path/to/requirements.txt" > requirements.dev.txt`
1. Install Mosheh with common install command: `#!sh pip install mosheh`
1. Write Mosheh to the dev requirements file: `#!sh echo mosheh >> requirements.dev.txt`

The full logic ends like this:

```sh
touch requirements.dev.txt
echo "-r ./path/to/requirements.txt" > requirements.dev.txt
pip install mosheh
echo mosheh >> requirements.dev.txt
```

!!! warning "Example Path Above"

    Just remember to update path to the real path on your case, just copying and pasting may not work because the used path is a mock one.

### Poetry

[Poetry](https://python-poetry.org/docs/) is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. **Poetry** offers a lockfile to ensure repeatable installs, and can build your project for distribution. Just like **uv**, **Poetry** is better than **PIP** because of its robust features list, ensuring more possibilities to automate and handle development processes. To install Mosheh with **Poetry** you can run the command below:

```sh
poetry add mosheh -G dev
```

Since `#!sh --dev` is now deprecated the documentation itself says to use `#!sh --group dev` `#!sh -G dev`. Being more specific you can also define Mosheh as documentation dependency, depending on how you wants to deal with it by running `#!sh poetry add mosheh -G docs`.

## Execution

As shown above, there are different ways to install Mosheh and the same happens when running it. In general cases calling `mosheh` on terminal already works, but depending on the installation method there are better options to execute the same script.

If using **PIP**, the way demonstraded below is suficient:

```sh
mosheh [-h] -root ROOT: Path \
      [--repo-name REPO_NAME: str] \
      [--repo-url REPO_URL: URL] \
      [--edit-uri EDIT_URI: str] \
      [--logo-path LOGO_PATH: Path] \
      [--readme-path README_PATH: Path] \
      [--verbose VERBOSE: Literal[0 | 1 | 2 | 3 | 4]] \
      [--output OUTPUT: Path]
```

Elif using **uv**, call `mosheh` from `uv run` to be concise with the ecosystem in use:

```sh
uv run mosheh [-h] -root ROOT: Path \
      [--repo-name REPO_NAME: str] \
      [--repo-url REPO_URL: URL] \
      [--edit-uri EDIT_URI: str] \
      [--logo-path LOGO_PATH: Path] \
      [--readme-path README_PATH: Path] \
      [--verbose VERBOSE: Literal[0 | 1 | 2 | 3 | 4]] \
      [--output OUTPUT: Path]
```

Elif using another method installation, remenber to check if there is support for running scripts by them or you should use `mosheh` directly from terminal.

## Parameters

The parameters for running Mosheh goes from the codebase root to the logging level. Here we are going to cover them in detail to be no doubt about the use of each one.

### `-root`

- Mandatory: `#!py Required`
- Type: `#!py Path`
- Default: `#!py None`

This represents the root dir, where Mosheh is going to start mining. To prevents it of search for files on a random directory or document undesired code, it's mandatory to tell where the search should start.

### `--repo-name`

- Mandatory: `#!py Optional`
- Type: `#!py str`
- Default: `#!py 'GitHub'`

This tells the repository name to be annotated in the generated documentation. Usually the used value is the repository username plus the project name, such as `reu/zerg` or `LucasGoncSilva/mosheh`.

### `--repo-url`

- Mandatory: `#!py Optional`
- Type: `#!py URL`
- Default: `#!py 'https://github.com/'`

As the name suggests, this one is for create the documentation with repo URL defined. Following the example above, it's value should be `https://github.com/reu/zerg` or `https://github.com/LucasGoncSilva/mosheh`.

### `--edit-uri`

- Mandatory: `#!py Optional`
- Type: `#!py str`
- Default: `#!py 'blob/main/documentation/docs'`

When you visits someone's GitHub repository, the URL is the well known `https://github.com/reu/zerg`. Once you go to view/update it, the `--edit-uri` comes to it: `https://github.com/reu/zerg/blob/master/Cargo.toml`. Since this is configured to the main branch and the specific dir `documentation/docs`, any file on this sub-path will be allowed for view or edit if your ptoject desires that.

### `--logo-path`

- Mandatory: `#!py Optional`
- Type: `#!py Path`
- Default: `#!py None`

There is no secret about this one. You passes the path to project's logo and Mosheh uses it as documentation logo. Just like this. If not provided, this will be using [Material MkDocs](https://squidfunk.github.io/mkdocs-material/) one.

### `--readme-path`

- Mandatory: `#!py Optional`
- Type: `#!py Path`
- Default: `#!py None`

There is also no secret about this one. You passes the path to project's `README.md` and Mosheh uses it as documentation Homepage. Just like this. If not provided, this wiil be using the default MkDocs index page content.

### `--output`

- Mandatory: `#!py Optional`
- Type: `#!py Path`
- Default: `#!py '.'`

Similar to `--root`, but for the generated documentation. The path provided here is the path to find the documentation at the end of the day. Not too much about this one.

### `--verbose`

- Mandatory: `#!py Optional`
- Type: `#!py int`
- Default: `#!py 3`

When running the script, may be util to see what's going on under the hoods... or not. For this case, `--verbose` comes to play allowing you to choose between different types of logging, from 0 to 4: `#!py logging.CRITICAL`, `#!py logging.ERROR`, `#!py logging.WARNING`, `#!py logging.INFO` and `#!py logging.DEBUG`.
