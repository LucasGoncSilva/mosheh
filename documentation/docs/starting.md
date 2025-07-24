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
mosheh [-h] [--verbose {0,1,2,3,4}] {init,run} ...
```

Elif using **uv**, call `mosheh` from `uv run` to be concise with the ecosystem in use:

```sh
uv run mosheh [-h] [--verbose {0,1,2,3,4}] {init,create} ...
```

## Commands

### Global Parameter

Apart from command-specific parameters, there’s also one global parameter that can (and should) be used to control output verbosity.

#### `--verbose`

- Mandatory: `#!py Optional`
- Type: `#!py int`
- Default: `#!py 3`

Controls the verbosity level of the CLI output, ranging from `0` to `4`:

- `#!py 0`: Quiet / Critical only
- `#!py 1`: Errors
- `#!py 2`: Warnings
- `#!py 3`: Default info level
- `#!py 4`: Full debug / oversharing

Use this flag depending on your context — whether you need clean output or full transparency for debugging and tracking.

Mosheh currently supports two main commands that represent its usage modes: `init` and `create`. Each has its own parameters, and there’s also a global one available across executions: `--verbose`.

### `init`

Initializes Mosheh by creating the configuration file that enables its usage. Nothing can be done without this config file with the name of `mosheh.json`

#### `--path`

- Mandatory: `#!py Optional`
- Type: `#!py str`
- Default: `#!py '.'`

Defines where the configuration file should be created. If nothing is informed, it defaults to the current directory (`.`). This allows flexibility to scaffold the config at any desired location inside the project. The config file generated is detailed below:

```json
{
  "documentation": {
    "projectName": "Mosheh",
    "repoName": "mosheh",
    "repoUrl": "https://github.com/lucasgoncsilva/mosheh",
    "editUri": "blob/main/documentation/docs",
    "siteUrl": "https://lucasgoncsilva.github.io/mosheh/",
    "logoPath": "./path/to/logo.svg",
    "readmePath": "./path/to/README.md",
    "codebaseNavPath": "Codebase"
  },
  "io": {
    "rootDir": "./app/",
    "outputDir": "./path/to/output/"
  }
}
```

#### Section `#!json "documentation"`

Documentation-related data

- `#!json "projectName"`: Name of the project (e.g. "Mosheh")
- `#!json "repoName"`: Name of the repository (e.g. "django-ninja")
- `#!json "repoUrl"`: URL of the repository (e.g. "https://github.com/matplotlib/matplotlib")
- `#!json "editUri"`: Editting URI (e.g. "blob/main/documentation/docs")
- `#!json "siteUrl"`: URL of the documentation website (path included if necessary)
- `#!json "logoPath"`: Relative path of the project's logo (inside repository)
- `#!json "readmePath"`: Relative path of the project's README (inside repository)
- `#!json "codebaseNavPath"`: Documentation path to the codebase section

#### Section `#!json "io"`

IO-related data

- `#!json "rootDir"`: Relative path for the codebase dir
- `#!json "outputDir"`: Relative path for the documentation output dir

### `create`

Mosheh's feature for codebase tracking and documentation creation. It runs the tool based on the configuration and setup defined. By reading the config file, evaluates the pointed codebase, registers it's data and generates the output file markdown for each file, writing every file to a path respecting the codebase path.

#### `--json`

- Mandatory: `#!py Optional`
- Type: `#!py str`
- Default: `#!py '.'`

Defines where to read the configuration file from. If not provided, it will assume the current directory. This parameter enables control over which config Mosheh should consider when running.

### `update`

Mosheh's feature for codebase tracking and documentation updating. It runs the tool based on the configuration and setup defined. Executes almost the same logic of `create` command, but just updating the codebase markdown files instead of creating the documentation from scratch.

#### `--json`

- Mandatory: `#!py Optional`
- Type: `#!py str`
- Default: `#!py '.'`

Defines where to read the configuration file from. If not provided, it will assume the current directory. This parameter enables control over which config Mosheh should consider when running.
