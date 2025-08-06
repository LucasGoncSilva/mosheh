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

Mosheh, automatic and elegant documentation of Python code with MkDocs.

Inspirated by `cargodoc` - a Rust tool for code documenting - and using [MkDocs](https://www.mkdocs.org/) + [Material MkDocs](https://squidfunk.github.io/mkdocs-material/), Mosheh is an **easy, fast, plug-and-play** tool which saves time while **automating** the process of documenting the **source code of a Python codebase**.

<!--
| Project/Codebase | PLoC  | Mosheh's Exec Time |         |
| ---------------- | ----- | ------------------ | ------- |
| Mosheh           | ~4k   |                    | 0.303s  |
| scikit-learn     | ~862k | ███████████        | 11.783s |
| NumPy            | ~204k | ████████████       | 12.205s |
 -->

<div style="display: grid; place-items: center;">
<table>
  <thead>
    <tr>
      <th>Project/Codebase</th>
      <th>PLoC</th>
      <th>Mosheh's Exec Time</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Mosheh</td>
      <td>~4k</td>
      <td></td>
      <td>0.303s</td>
    </tr>
    <tr>
      <td>scikit-learn</td>
      <td>~862k</td>
      <td>███████████</td>
      <td>11.783s</td>
    </tr>
    <tr>
      <td>NumPy</td>
      <td>~204k</td>
      <td>████████████</td>
      <td>12.205</td>
    </tr>
  </tbody>
</table>
</div>

> PLoC: Python Lines of Code

> Specs: Mint 21.3 | Aspire A515-54 | Intel i7-10510U (8) @ 4.900GHz | RAM 19817MiB

- **Fast**: Documented NumPy (200k+ Python LoC) in just 12.2 seconds
- **Simple**: No complex logic behind the scenes — easy to understand and trust
- **Easy to Use**: No advanced knowledge required — document any Python codebase effortlessly
- **Plug and Play**: No need to modify your codebase — just install Mosheh, `init`, configure `mosheh.json` and `create`
- **Professional**: Generates MkDocs Material-based documentation — a clean, responsive, and professional website by default
- **Modern**: Designed for modern Python — fully type-hint-aware and built using the latest Python best practices
- **Scalable**: Handles small scripts to massive codebases without performance issues
- **Flexible**: Works with any Python structure — does not enforce docstring formats or architectural patterns
- **Open Source**: Free to use, fully open-source under the MIT license, and built with community in mind
- **Integrable**: Easy to embed into CI/CD pipelines or project scaffolds for automatic documentation generation

![Visual demonstration of Mosheh](https://raw.githubusercontent.com/LucasGoncSilva/mosheh/refs/heads/main/.github/demo.gif)

This is not an alternative to MkDocs, but a complement based on it, since Mosheh lists all files you points to, saves every single notorious definition statement on each file iterated, all using Python `ast` native module for handling the AST and then generating a modern documentation respecting the dirs and files hierarchy.

At the moment, Mosheh documents only Python files (`.py`, `.pyi`), where the stuff documented for each file is shown below:

- Imports `ast.Import | ast.ImportFrom`

  - [x] Type `Native | TrdParty | Local`
  - [x] Path (e.g. `math.sqrt`)
  - [x] Code

- Constants `ast.Assign | ast.AnnAssign`

  - [x] Name (token name)
  - [x] Typing Annotation (datatype)
  - [x] Value (literal or call)
  - [x] Code

- Classes `ast.ClassDef`

  - [x] Description (docstring)
  - [x] Name (class name)
  - [x] Parents (inheritance)
  - [ ] Methods Defined (nums and names)
  - [x] Code

- Funcs `ast.FunctionDef | ast.AsyncFunctionDef`

  - [x] Description (docstring)
  - [x] Name (func name)
  - [x] Type `Func | Method | Generator | Coroutine`
  - [x] Parameters (name, type, default)
  - [x] Return Type (datatype)
  - [ ] Raises (exception throw)
  - [x] Code

- Assertions `ast.Assert`

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

## Contributing

Before getting access to the To-Do List, Coding Style or even forking the project, we **strongly recommend** reading [Mosheh's Guidelines](https://lucasgoncsilva.github.io/mosheh/guidelines/)

## Arch

Mosheh's architecture can be interpreted in two ways: the directory structure and the interaction of the elements that make it up. A considerable part of a project is - or at least should be - that elements that are dispensable for its functionality are in fact dispensable, such as the existence of automated tests; they are important so that any existing quality process is kept to a minimum acceptable level, but if all the tests are deleted, the tool still works.

Here it is no different, a considerable part of Mosheh is, in fact, completely dispensable; follow below the structure of directories and relevant files that are part of this project:

```sh
.
├── mosheh/                     # Mosheh's source-code
│   ├── commands/*              # Logics for each command
│   ├── handlers/*              # Codebase handlers for each file
│   ├── doc/*                   # Documentation build logics
│   ├── types/                  # Custom data types
│   │   ├── basic.py            # Basic types (e.g. "type Token = str")
│   │   ├── contracts.py        # Contracts to ensure correct typing
│   │   ├── enums.py            # Enums for standardizing assignments
│   │   └── jsoncfg.py          # JSON for structuring commands config
│   ├── codebase.py             # Codebase reading logic
│   ├── constants.py            # Constants to be evaluated
│   ├── main.py                 # Entrypoint
│   └── utils.py                # Utilities
│
├── tests/                      # Template dir for testing
│   ├── DOC                     # Doc output dir
│   ├── PROJECT                 # Template project dir
│   └── unittest                # Automated tests
│
├── documentation/              # Mosheh's documentation dir
│   ├── docs/                   # Dir containing .md files and assets
│   ├── mkdocs.yml              # MkDocs's config file
│   └── mosheh.json             # Mosheh's exec config file
│
├── pyproject.toml              # Mosheh's config file for almost everything
├── uv.lock                     # uv's lockfile for dealing with dependencies
├── .python-version             # Default Python's version to use
│
├── .github/                    # Workflows and social stuff
│
├── LICENSE                     # Legal stuff, A.K.A donut sue me
│
└── .gitignore                  # Git "exclude" file
```

It is to be expected that if the `tests/` directory is deleted, Mosheh's core will not be altered in any way, so much so that when a tool is downloaded via `pip` or similar, the tool is not accompanied by tests, licenses, development configuration files or workflows. So, to help you understand how the `mosheh/` directory works, here's how the functional elements interact with each other:

![Flowchart diagram](https://raw.githubusercontent.com/lucasGoncSilva/mosheh/refs/heads/main/.github/flowchart.svg)

## Usage

After installing Mosheh as a development dependency, create the documentation folder if not exists and run `mosheh init [--path .]`; this will result in a `mosheh.json` config file just as below:

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

After making sure the data on that JSON reflects the desired (more about this file at the official documentation), running `mosheh create [--json .]` results in a documentation following the default MkDocs structure with Material MkDocs as theme, with the codebase documented over "Codebase" named-section.

## Development

### Installing Dependencies

```sh
# Automatically handles everything with .venv
uv sync
```

### Running Locally

```sh
# For running using uv and dealing with Mosheh as a module
uv run mosheh -h
```

### Building Locally

```sh
# Build pip-like file
uv build
```

### Testing

```sh
# Run all the testing workflow
uv run task test
```

### Lint

```sh
# Run all the linting workflow
uv run task lint
```

### Generate Self Document

```sh
# Generate Mosheh's Codebase Documentation
uv run task makedoc
```

## License

This project is under [MIT License](https://choosealicense.com/licenses/mit/). A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
