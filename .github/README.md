<h1 align="center">
  <img src="https://raw.githubusercontent.com/lucasGoncSilva/mosheh/refs/heads/main/.github/logo.svg" height="300" width="300" alt="Logo Mosheh" />
  <br>
  Mosheh
</h1>

![PyPI - Version](https://img.shields.io/pypi/v/mosheh?labelColor=101010)
![GitHub License](https://img.shields.io/github/license/LucasGoncSilva/mosheh?labelColor=101010)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LucasGoncSilva/mosheh/unittest.yml?labelColor=101010)

[![Changelog](https://img.shields.io/badge/here-here?style=for-the-badge&label=changelog&labelColor=101010&color=fff)](https://github.com/LucasGoncSilva/mosheh/blob/main/.github/CHANGELOG.md)

[![PyPI](https://img.shields.io/badge/here-here?style=for-the-badge&label=PyPI&labelColor=3e6ea8&color=f3e136)](https://pypi.org/project/mosheh/)

Mosheh, a tool for creating docs for projects, from Python to Python.

Basically, Mosheh lists all files you points to, saves every single notorious statement of definition on each file iterated, all using Python `ast` native module for handling the AST and then generating with [MkDocs](https://www.mkdocs.org/) and [Material MkDocs](https://squidfunk.github.io/mkdocs-material/) a documentation respecting the dirs and files hierarchy. The stuff documented for each file are listed below:

- Imports `[ast.Import | ast.ImportFrom]`

  - [x] Type `[Native | TrdParty | Local]`
  - [x] Path (e.g. 'django.http')
  - [x] Code

- Constants `[ast.Assign | ast.AnnAssign]`

  - [x] Name (token name)
  - [x] Typing Notation (datatype)
  - [x] Value (literal or call)
  - [x] Code

- Classes `[ast.ClassDef]`

  - [x] Description (docstring)
  - [x] Name (class name)
  - [x] Parents (inheritance)
  - [ ] Methods Defined (nums and names)
  - [ ] Example (usage)
  - [x] Code

- Funcs `[ast.FunctionDef | ast.AsyncFunctionDef]`

  - [x] Description (docstring)
  - [x] Name (func name)
  - [x] Type `[Func | Method | Generator | Coroutine]`
  - [x] Parameters (name, type, default)
  - [x] Return Type (datatype)
  - [ ] Raises (exception throw)
  - [ ] Example (usage)
  - [x] Code

- Assertions `[ast.Assert]`

  - [x] Test (assertion by itself)
  - [x] Message (opt. message in fail case)
  - [x] Code

## Stack

![Python](https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=ffd43b)

![uv](https://img.shields.io/badge/uv-2b0231?style=for-the-badge&logo=uv)
![Ruff](https://img.shields.io/badge/Ruff-2b0231?style=for-the-badge&logo=ruff)
![Material for MkDocs](https://img.shields.io/badge/Material%20for%20MkDocs-fff?style=for-the-badge&logo=material-for-mkdocs&logoColor=526cfe)

![GitHub](https://img.shields.io/badge/GitHub-fff?style=for-the-badge&logo=github&logoColor=181717)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-fff?style=for-the-badge&logo=github-pages&logoColor=222222)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088ff?style=for-the-badge&logo=github-actions&logoColor=fff)

## ToDo List

- [ ] Evaluate use of Rust for better proccessing
- [ ] Evaluate the processing of more files than just Python ones (e.g. `.txt`, `.toml`)
- [x] Migrate dependency system to use [uv](https://docs.astral.sh/uv/)
- [x] Process 25% of Python [AST](https://docs.python.org/3/library/ast.html)'s nodes on `mosheh.handler`
- [x] Process 50% of Python [AST](https://docs.python.org/3/library/ast.html)'s nodes on `mosheh.handler`
- [x] Process 75% of Python [AST](https://docs.python.org/3/library/ast.html)'s nodes on `mosheh.handler`
- [x] Process 100% of Python [AST](https://docs.python.org/3/library/ast.html)'s nodes on `mosheh.handler`
- [ ] Accept structured file (e.g. `mosheh.json`) as parameters replacement
- [ ] Provide an "exclude" config for files/dirs to ignore
- [ ] Insert `tags` for `.md` based on their names/contexts
- [ ] Get and list all metrics of above's statements featured
- [ ] Check for files docstrings and write below filepath
- [ ] Create detail page for classes with docstring and listing class constants and methods
- [ ] Create detail page for functions with docstring and body detail

## Arch

Mosheh's architecture can be interpreted in two ways: the directory structure and the interaction of the elements that make it up. A considerable part of a project is - or at least should be - that elements that are dispensable for its functionality are in fact dispensable, such as the existence of automated tests; they are important so that any existing quality process is kept to a minimum acceptable level, but if all the tests are deleted, the tool still works.

Here it is no different, a considerable part of Mosheh is, in fact, completely dispensable; follow below the structure of directories and relevant files that are part of this project:

```sh
.
├── mosheh                      # Mosheh's source-code
│   ├── codebase.py             # Codebase reading logic
│   ├── constants.py            # Constants to be evaluated
│   ├── custom_types.py         # Custom data types
│   ├── doc.py                  # Documentation build logic
│   ├── handlers.py             # Codebase nodes handlers functions
│   ├── main.py                 # Entrypoint
│   ├── metadata.py             # Metadata about Mosheh itself
│   └── utils.py                # Utilities
│
├── tests                       # Template dir for testing
│   ├── DOC                     # Doc output dir
│   ├── PROJECT                 # Template project dir
│   └── unittest                # Automated tests
│
├── documentation               # Mosheh's documentation dir
│   ├── docs                    # Dir containing .md files and assets
│   └── mkdocs.yml              # MkDocs config file
│
├── pyproject.toml              # Mosheh's config file for almost everything
├── uv.lock                     # uv's lockfile for dealing with dependencies
├── .python-version             # Default Python's version to use
│
├── .github                     # Workflows and social stuff
│
├── LICENSE                     # Legal stuff, A.K.A donut sue me
│
└── .gitignore                  # Git "exclude" file
```

It is to be expected that if the `tests/` directory is deleted, Mosheh itself will not be altered in any way, so much so that when a tool is downloaded via `pip` or similar, the tool is not accompanied by tests, licenses, development configuration files or workflows. So, to help you understand how the `mosheh/` directory works, here's how the functional elements interact with each other:

![Flowchart diagram](https://raw.githubusercontent.com/lucasGoncSilva/mosheh/refs/heads/main/.github/flowchart.svg)

## Usage

### Local Build and Installation

#### Installing Dependencies

```sh
pip install uv  # For installing uv to handle the environment

uv sync  # Automatically creates a .venv, activates it and install libs based on uv.lock and pyproject.toml
```

#### Runing Locally

```sh
uv run -m mosheh.main  # For running using uv and dealing with Mosheh as a module
```

#### Installing Locally

```sh
uv build  # Build pip-like file

uv pip install dist/mosheh-<VERSION>-py3-none-any.whl --force-reinstall  # Install Mosheh using generated pip-like file
```

### Testing

```sh
uv run pytest  # Run pytest
```

### Parameters

|      Call       |  Type  | Mandatory  | Default                          | Example                         | Description                                                      |
| :-------------: | :----: | :--------: | :------------------------------- | :------------------------------ | :--------------------------------------------------------------- |
| `-h`, `--help`  | `str`  | `Optional` | `None`                           | `-h`, `--help`                  | Help message                                                     |
|     `-root`     | `Path` | `Required` | `None`                           | `-root example/`                | Root dir, where the analysis starts.                             |
|  `--repo-name`  | `str`  | `Optional` | `'GitHub'`                       | `--repo-name toicin`            | Name of the code repository to be mapped.                        |
|  `--repo-url`   | `URL`  | `Optional` | `'https://github.com/'`          | `--repo-url https://random.com` | URL of the code repository to be mapped.                         |
|  `--edit-uri`   | `str`  | `Optional` | `'blob/main/documentation/docs'` | `--edit-uri blob/main/docs`     | URI to view raw or edit blob file.                               |
|  `--logo-path`  | `Path` | `Optional` | `None`                           | `--repo-url .github/logo.svg`   | Path for doc/project logo, same Material MkDocs's formats.       |
| `--readme-path` | `Path` | `Optional` | `None`                           | `--repo-url .github/README.md`  | Path for `README.md` file to used as homepage.                   |
|   `--verbose`   | `int`  | `Optional` | `3` - `logging.INFO`             | `--verbose 4`                   | Verbosity level, from 0 (quiet/critical) to 4 (overshare/debug). |
|   `--output`    | `Path` | `Optional` | `'.'` - current dir              | `--output doc/`                 | Path for documentation output, where to be created.              |

## License

This project is under [MIT License](https://choosealicense.com/licenses/mit/). A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
