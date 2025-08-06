# Changelog and Update History

A changelog is a document that tracks the history of changes in a project, typically organized by version numbers. It serves as a transparent record for developers, users, and contributors, detailing what has been added, updated, fixed, removed, or addressed in terms of security. By offering a structured overview, changelogs play a vital role in maintaining trust, facilitating communication, and easing version management.

Changelogs provide a transparent narrative of a project’s evolution. They ensure users can make informed decisions about updating software and give contributors insights into the project’s direction. For development teams, changelogs are invaluable for version control and accountability. Well-maintained changelogs foster trust, improve user engagement, and ensure smoother project management for all stakeholders.

Key Components of a Changelog:

- Adds: This section highlights new features, tools, or functionalities introduced to the project. For example, a CLI tool may include a new command or configuration option. Clearly listing these additions allows users to discover improvements and expanded capabilities.
- Updates: Updates reflect modifications or enhancements to existing features, such as performance optimizations or UI/UX improvements. These entries help users understand what has evolved, ensuring they benefit from improved usability or efficiency.
- Fixes: Fixes document the resolution of bugs or issues. By specifying what was corrected, users gain confidence that problems they may have encountered have been addressed, reducing frustration.
- Deprecates: When something (function, approach or even feature) is replaced but still available, usually for retrocompatibility, this thing is marked as deprecated; the idea is to remove later without breaking existing use cases.
- Removes: Sometimes, features or functionalities are removed. Listing these changes prevents surprises, enabling users to adapt and refactor their workflows accordingly.
- Security: Security changes focus on vulnerabilities that have been mitigated or resolved. This section reassures users that the project maintains high standards for safety and data protection.

---

<!--

## {VERSION} - {DATE}

### Adds

- Item

### Updates

- Item

### Fixes

- Item

### Deprecates

- Item

### Removes

- Item

### Security

- Item

-->

## v2.0.2 - 2025-08-06

### Adds

- Features list to `README.md`

### Updates

- Refactor `_handle_node` for improved performance and readability by using `ast.unparse` directly - [PR 13](https://github.com/LucasGoncSilva/mosheh/pull/13) - [@MananJain39](https://github.com/MananJain39)
- Moved homepage logic to `mosheh.doc.shared`
- Test suite updates with [Hypothesis](https://hypothesis.readthedocs.io/en/latest/)

### Fixes

- Small documentation issues, such as Discussion Templates titles

### Removes

- Remove unused `_handle_general` function after refactoring - [PR 13](https://github.com/LucasGoncSilva/mosheh/pull/13) - [@MananJain39](https://github.com/MananJain39)
- Remove unnecessary `typing.cast` calls - [PR 13](https://github.com/LucasGoncSilva/mosheh/pull/13) - [@MananJain39](https://github.com/MananJain39)

## v2.0.1 - 2025-07-30

### Adds

- `.github/DISCUSSION_TEMPLATE` files for discussion templates: "Questions", "Showcases" and "Ideas to Features"

### Updates

- Replaced manual binary search implementation with `bisect.bisect_left` wrapper in `utils.bin` - [PR 7](https://github.com/LucasGoncSilva/mosheh/pull/7) - [@ClanEver](https://github.com/ClanEver)
- Refactored dataclass implementations to use NamedTuple - [PR 6](https://github.com/LucasGoncSilva/mosheh/pull/6) - [@ClanEver](https://github.com/ClanEver)
- Updated method calls from `.as_dict` to `._asdict()` - [PR 6](https://github.com/LucasGoncSilva/mosheh/pull/6) - [@ClanEver](https://github.com/ClanEver)

### Fixes

- `README.md` gif of Mosheh use

## v2.0.0 - 2025-07-24

### Adds

- Social `.github` files such as templates and guidelines (`ISSUE_TEMPLATE/`, `TODO.md`, ...)
- `py.typed` for defining Mosheh as a typed project
- New command `mosheh update --json .` for updating an existing codebase documentation

### Updates

- CLI interface from simple commands to new logic with `init`, `create` and `mosheh.json`
- `README.md` and other documentation properly updated
- `mosheh.custom_types` divided into `mosheh.types` with `basic`, `contracts`, `jsoncfg` and `enums`
- Enums inheritance change from `enum.Enum` to `enum.StrEnum`
- `mosheh.types.basic` definition using `type` keyword
- `handler.py` moved to `/handlers/python.py` for future convenience
- `mosheh.handlers.python.handle_def_nodes` renamed to `handle_std_nodes`
- `mosheh.handlers.python._handle_general` for dealing with `ast.AST` not defined on `types.contracts`
- `commands/*` to deal with different commands instead of `main.py` raw logic
- General docstring for new and updated files/functions/classes

### Fixes

- Rename variables with duplicated names
- File path with `.dir` managed to `dir`
- "Notation" into "Annotation" writing over codebase

### Removes

- `mosheh.handler` internal funcs but the ones called by `mosheh.handler.handle_std_nodes`

## v1.3.4 - 2025-01-07

### Adds

- File docstrings for source code, documenting the file role
- File docstrings now observed and inserted into output documentation markdown

### Updates

- Mosheh now requires Python 3.13
- Dependencies now supports versions in `lib>=x.x.x` style, no more `lib==x.x.x` only
- `mosheh.doc` functions `__write_to_file` to `_write_to_file` and `__update_navigation` to `_update_navigation`

### Fixes

- `'.'` added to generated documentation files and dirs on `mosheh.doc` creation lines

## v1.3.3 - 2024-12-27

### Adds

- "Role" defined and added to markdown generated doc files
- Functions now has docstring description on markdown

### Updates

- Codebase readed files now documented under `- Codebase` section on generated `mkdocs.yml`

### Security

- `f'{name}'` to `f'{name}'` on `tests.PROJECT.dummy.views.index` test example

## v1.3.2 - 2024-12-17

### Adds

- `_mark_methods` created on `mosheh.codebase` plus `encapsulated_mark_methods_for_unittest` for testing
- Examples for `mosheh.handler` functions on docstrings

### Updates

- Sequence-like `mosheh.constants` constants sorted in code to better performing

### Fixes

- Implementing `rich` as direct dependency

## v1.3.1 - 2024-12-16

### Adds

- Publish official documentation website: [https://lucasgoncsilva.github.io/mosheh/](https://lucasgoncsilva.github.io/mosheh/)

### Updates

- Remaking the Mosheh's documentation itself
- Setting documentation website metadata on `pyproject.toml`
- `mosheh.constants` constants `BUILTIN_MODULES`, `BUILTIN_FUNCTIONS`, `BUILTIN_DUNDER_METHODS` and `ACCEPTABLE_LOWER_CONSTANTS` from `typing.Iterator` to `typing.Sequence`

## v1.3.0 - 2024-12-13

### Adds

- Handler functions to deal with statements not defined before, such as `ast.For` - all below:

|   Added Nodes   |                 |                     |                    |                 |                      |
| :-------------: | :-------------: | :-----------------: | :----------------: | :-------------: | :------------------: |
| `ast.AsyncFor`  | `ast.AsyncWith` |   `ast.AugAssign`   |    `ast.Await`     |   `ast.Break`   |    `ast.Continue`    |
|    `ast.Del`    |  `ast.Delete`   | `ast.ExceptHandler` |     `ast.Expr`     |    `ast.For`    | `ast.FormattedValue` |
|  `ast.Global`   |    `ast.If`     |     `ast.Load`      |    `ast.Match`     | `ast.NamedExpr` |    `ast.Nonlocal`    |
| `ast.ParamSpec` |   `ast.Pass`    |     `ast.Raise`     |    `ast.Return`    |  `ast.Starred`  |     `ast.Store`      |
|  `ast.TryStar`  |    `ast.Try`    |   `ast.TypeAlias`   | `ast.TypeVarTuple` |  `ast.TypeVar`  |     `ast.While`      |
|   `ast.With`    | `ast.YieldFrom` |     `ast.Yield`     |

- `rtype` or return type annotation on `tests.unittest` test functions
- New theme to Mosheh's self documentation code blocks inspired by [Dracula Theme](https://draculatheme.com/)
- Insert logs on all the Mosheh's codebase using `mosheh.set_logging_config` and native `logging`:
  - CRITICAL: when something crashes the script
  - ERROR: non-crashing errors on the script
  - WARNING: notorious advising that are not errors
  - INFO: normal log level
  - DEBUG: detailed step-by-step execution

### Updates

- `mosheh.handler._handle_node` now can handle nodes off all types listed above
- `ast.FunctionDef` inside of `ast.ClassDef` now with `FunctionType.Method` attribute on output doc

### Removes

- `Statement` class from `mosheh.custom_types` unused types, such as `Statement.Call` - all below:

|  Removed Types   |                  |                      |
| :--------------: | :--------------: | :------------------- |
| `BinOp = auto()` | `Call = auto()`  | `Compare = auto()`   |
| `List = auto()`  |  `Set = auto()`  | `Tuple = auto()`     |
| `Dict = auto()`  | `Slice = auto()` | `Subscript = auto()` |

## v1.2.1 - 2024-12-10

### Adds

- Unittest workflow for automated tests using `pytest`: `.github/workflows/unittest.yml`
- PyPI publishing workflow for new public versions using `uv` and `twine`: `.github/workflows/publish_pypi.yml`
- MkDocs publishing workflow for updating documentation using `uv` and `mkdocs`: `.github/workflows/publish_mkdocs.yml`
- New badges for `README.md` "Stack" section: Material for MkDocs, GitHub, GitHub Pages and GitHub Actions
- `[build-system]`, `[project.urls]`, `[project.scripts]` and some other small infos inserted on `pyproject.toml`

### Updates

- Reordering Stack badges for `README.md`

### Fixes

- `mosheh` back as script entrypoint for Mosheh in `pyproject.toml` config file

### Removes

- `setup.py` deleted due total substitution by `pyproject.toml`

## v1.2.0 - 2024-12-10

### Adds

- Test file for `mosheh.utils` functions: `tests.unittest.utils`
- Test file for `mosheh.constants` constants: `tests.unittest.constants`
- Test file for `mosheh.doc` functions: `tests.unittest.doc`
- Test file for `mosheh.handler` functions: `tests.unittest.handler`
- Mock test file `mock.py.txt` for serving `tests.unittest.handler` as template

### Updates

- `pyproject.toml` setting `pytest` to use `-vv` parameter
- `list[Any] | tuple[Any]` to `collections.abc.Sequence[Any]` on `mosheh.utils.bin:universe` arg
- `dict[Any, Any]` to `defaultdict[Any, Any]` on `mosheh.utils.nested_dict` rtype
- `dict[Any, Any]` to `defaultdict[Any, Any]` on `mosheh.utils.add_to_dict:structure` arg and rtype
- Changing all `moshe.doc` functions except `create_doc` to be private (e.g. `_process_file`)
- Changing all `moshe.handlers` functions except `handle_std_nodes` to be private (e.g. `_process_file`)
- Renaming `moshe.handlers` to `moshe.handler`
- Changing `moshe.codebase.iterate` to be private: `moshe.codebase._iterate`

### Fixes

- `Proccess` word refined to `Process`

## v1.1.1 - 2024-12-06

### Adds

- `metadata.py` created to separate metadata from the actual `main.py` file

### Updates

- Migration from `pip`/`requirements.txt` dependency management to `uv`/`pyproject.toml`/`uv.lock`/`.python-version`
- `documentation/*.md` files formatted
- `README.md` updated with new local installation and running instructions
- `README.md` updated with new dependency management system into dir's demonstration
- Substituting `handlers.py`'s `typing.Optional` to `... | None` (e.g. `Optional[str]` to `str | None`)

### Removes

- `ruff.toml` deleted due to `pyproject.toml` creation

## v1.1.0 - 2024-12-06

### Adds

- Creation of `CHANGELOG.md`
- `setup.py` into `README.md` dir's demonstration
- `documentation` into `README.md` dir's demonstration
- `--edit-uri` parameter defined as `'blob/main/documentation/docs'`

### Updates

- `README.md`'s todo list targets
- `--exit` parameter renamed to `--output`
- `--logo-path` argument's defaults to `None`
- `--readme-path` argument's defaults to `None`
- `clickable_checkbox` statement of `mkdocs.yml` defaults to `false`
- Some function docstrings reviewed

## v1.0.0 - 2024-12-04

### Adds

- First stable version release
