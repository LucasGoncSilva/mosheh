<h1 align="center">
  <img src="https://raw.githubusercontent.com/lucasGoncSilva/mosheh/refs/heads/main/.github/logo.svg" height="300" width="300" alt="Logo Mosheh" />
  <br>
  Mosheh
</h1>

![GitHub License](https://img.shields.io/github/license/LucasGoncSilva/mosheh?labelColor=101010)

<!-- ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LucasGoncSilva/mosheh/XXXXXX.yml?style=flat&labelColor=%23101010) -->

Mosheh is a tool for generating documentations for projects, from Python to Python.

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

```mermaid
flowchart LR

subgraph YOUR_ENV
  gen_doc[/"Generated Doc"/]:::Other
  base[/"Project"/]:::Other
end

subgraph MOSHEH
  main("main.py"):::Mosheh
  codebase("codebase.py"):::Mosheh
  handlers("handlers.py"):::Mosheh
  types{{"custom_types.py"}}:::Mosheh
  utils{{"utils.py"}}:::Mosheh
  const("constants.py"):::Mosheh
  doc("doc.py"):::Mosheh
end


const -..-> doc
types -.-> main & codebase & utils & handlers & doc
handlers -.-> codebase
utils -.-> codebase & doc & handlers

base --> main
main --> codebase
codebase --> doc
doc --> gen_doc


style YOUR_ENV fill:#057,color:#ffde57,stroke:#ffde57;
style MOSHEH fill:#1a1a1a,color:#fff,stroke:#808080;

classDef Other fill:#ffde57,color:#057,stroke:#057;
classDef Mosheh fill:#404040,color:#fff,stroke:#ccc;

linkStyle default stroke:#808080
linkStyle 10,11,12,13 stroke:#fff
```

## Commands and Parameters

### Commands

To be defined.

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

## Licença

This project is under [MIT License](https://choosealicense.com/licenses/mit/). A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
