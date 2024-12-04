<h1 align="center">
  <img src="https://raw.githubusercontent.com/lucasGoncSilva/mosheh/refs/heads/main/.github/logo.svg" height="300" width="300" alt="Logo Mosheh" />
  <br>
  Mosheh
</h1>

![GitHub License](https://img.shields.io/github/license/LucasGoncSilva/mosheh?labelColor=101010)

<!-- ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LucasGoncSilva/mosheh/XXXXXX.yml?labelColor=%23101010) -->

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

  - [ ] Description (docstring)
  - [x] Name (class name)
  - [x] Parents (inheritance)
  - [ ] Methods Defined (nums and names)
  - [ ] Example (usage)
  - [x] Code

- Funcs `[ast.FunctionDef | ast.AsyncFunctionDef]`

  - [ ] Description (docstring)
  - [x] Name (func name)
  - [ ] Type `[Func | Method | Generator | Coroutine]`
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

![Python logo](https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=FFD43B)

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
│   └── utils.py                # Utilities
│
├── tests                       # Template dir for testing
│   ├── DOC                     # Doc output dir
│   └── PROJECT                 # Template project dir
│
├── requirements.txt            # Mosheh's dependencies
│
├── .github                     # Workflows and social stuff
│
├── LICENSE                     # Legal stuf, A.K.A donut sue me
│
├── ruff.toml                   # Ruff config file
│
└── .gitignore                  # Git "exclude" file
```

It is to be expected that if the `tests/` directory is deleted, Mosheh itself will not be altered in any way, so much so that when a tool is downloaded via `pip` or similar, the tool is not accompanied by tests, licenses, development configuration files or workflows. So, to help you understand how the `mosheh/` directory works, here's how the functional elements interact with each other:

![Flowchart diagram](https://raw.githubusercontent.com/lucasGoncSilva/mosheh/refs/heads/main/.github/flowchart.svg)

## Usage

### Local Build and Installation

```sh
pip install -r requirements.txt  # Install all dependencies in your local environment

# or

pip install wheel setuptools  # Install only build dependencies in your local environment
```

```sh
python3 setup.py sdist bdist_wheel  # Build pip-like file

pip install dist/mosheh-<VERSION>-py3-none-any.whl --force-reinstall  # Install Mosheh using generated pip-like file
```

### Running

```sh
mosheh [-h] -root ROOT [--repo-name REPO_NAME] [--repo-url REPO_URL] [--logo-path LOGO_PATH] [--readme-path README_PATH] [--exit EXIT]
```

### Parameters

|      Call       | Type  | Mandatory  |         Default         | Example                         | Action                           |
| :-------------: | :---: | :--------: | :---------------------: | :------------------------------ | :------------------------------- |
| `-h`, `--help`  | `str` | `Optional` |         `None`          | `-h`, `--help`                  | Help message                     |
|     `-root`     | `str` | `Required` |         `None`          | `-root example/`                | Root to start looking for        |
|  `--repo-name`  | `str` | `Optional` |       `'GitHub'`        | `--repo-name toicin`            | Repo name                        |
|  `--repo-url`   | `str` | `Optional` | `'https://github.com/'` | `--repo-url https://random.com` | Repo URL                         |
|  `--logo-path`  | `str` | `Optional` |          `''`           | `--repo-url .github/logo.svg`   | Path to project logo             |
| `--readme-path` | `str` | `Optional` |          `''`           | `--repo-url .github/README.md`  | Path to project `README.md` file |
|    `--exit`     | `str` | `Optional` |          `'.'`          | `--exit doc/`                   | Doc output path                  |

## License

This project is under [MIT License](https://choosealicense.com/licenses/mit/). A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
