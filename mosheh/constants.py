"""
This module defines constants and templates used throughout the project.

It aims to standardize project-wide values, ensure consistency, and streamline the
development and documentation process.

The constants defined here are:

1. `BUILTIN_MODULES`: A comprehensive `sorted` object of Python's built-in modules for
    reference or validation purposes.

2. `BUILTIN_FUNCTIONS`: A `sorted` object of Python's built-in functions to support
    validation, documentation or tooling needs.

3. `BUILTIN_DUNDER_METHODS`: A `sorted` object commonly used double-underscore (dunder)
    methods in Python, aiding in validation or documentation.

4. `ACCEPTABLE_LOWER_CONSTANTS`: Lowercase constants acceptable in the project to
    enforce naming conventions.

5. `DEFAULT_MKDOCS_YML`: A template for MkDocs configuration using the Material theme,
    with custom settings for a consistent and professional documentation structure.

6. Markdown Templates:
    * Files (`FILE_MARKDOWN`)
    * Imports (`IMPORT_MD_STRUCT`)
    * Assignments (`ASSIGN_MD_STRUCT`)
    * Classes (`CLASS_DEF_MD_STRUCT`)
    * Functions (`FUNCTION_DEF_MD_STRUCT`)
    * Assertions (`ASSERT_MD_STRUCT`)

These constants can be imported and reused wherever needed in the project. Be careful
when updating this file to maintain consistency across the project. Remember that this
file should remain immutable during runtime and utilize Python's `typing.Final` type
hint to mark constants as non-overridable.
"""

import builtins
from inspect import isclass
from pkgutil import iter_modules
from sys import builtin_module_names
from sysconfig import get_paths
from types import BuiltinFunctionType
from typing import Final


BUILTIN_MODULES: Final[list[str]] = sorted(
    set(builtin_module_names)
    | {name for _, name, _ in iter_modules([get_paths()['stdlib']])}
)

BUILTIN_FUNCTIONS: Final[list[str]] = sorted(
    i
    for i in dir(builtins)
    if isinstance(getattr(builtins, i), BuiltinFunctionType)
    or isinstance(getattr(builtins, i), type)
    and not (
        isinstance(getattr(builtins, i), type)
        and issubclass(getattr(builtins, i), BaseException)
    )
)

BUILTIN_DUNDER_METHODS: Final[list[str]] = sorted(
    attr
    for name in dir(builtins)
    if isclass(getattr(builtins, name))
    for attr in dir(getattr(builtins, name))
    if attr.startswith('__') and attr.endswith('__')
)

ACCEPTABLE_LOWER_CONSTANTS: Final[tuple[str, ...]] = (
    '__author__',
    '__copyright__',
    '__credits__',
    '__date__',
    '__email__',
    '__keywords__',
    '__license__',
    '__maintainer__',
    '__repository__',
    '__status__',
    '__version__',
    'app',
    'app_name',
    'application',
    'main',
    'urlpatterns',
)

DEFAULT_MKDOCS_YML: Final[str] = """site_name: {proj_name}
repo_url: {repo_url}
repo_name: {repo_name}
edit_uri: "{edit_uri}"


theme:
  name: material
  language: en
  favicon: {logo_path}
  logo: {logo_path}
  font:
    text: Ubuntu

  icon:
    next: fontawesome/solid/arrow-right
    previous: fontawesome/solid/arrow-left
    top: fontawesome/solid/arrow-up
    repo: fontawesome/brands/git-alt
    edit: material/pencil
    view: material/eye

    tag:
      homepage: fontawesome/solid/house
      index: fontawesome/solid/file
      overview: fontawesome/solid/binoculars
      test: fontawesome/solid/flask-vial
      infra: fontawesome/solid/server
      doc: fontawesome/solid/book
      legal: fontawesome/solid/scale-unbalanced
      user: fontawesome/solid/user
      API: fontawesome/solid/gears
      browser: fontawesome/solid/desktop

    admonition:
      note: fontawesome/solid/note-sticky
      abstract: fontawesome/solid/book
      info: fontawesome/solid/circle-info
      tip: fontawesome/solid/fire-flame-simple
      success: fontawesome/solid/check
      question: fontawesome/solid/circle-question
      warning: fontawesome/solid/triangle-exclamation
      failure: fontawesome/solid/xmark
      danger: fontawesome/solid/skull
      bug: fontawesome/solid/bug
      example: fontawesome/solid/flask
      quote: fontawesome/solid/quote-left

  palette:
    # Palette toggle for light mode
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Light/Dark Mode
      primary: green
      accent: indigo

    # Palette toggle for dark mode
    - scheme: slate
      toggle:
        icon: material/brightness-3
        name: Light/Dark Mode
      primary: teal
      accent: orange


  features:
    - navigation.indexes
    - navigation.tabs
    - navigation.top
    - header.autohide
    - navigation.footer
    - content.action.view
    - content.action.edit
    - announce.dismiss
    - content.tabs.link


markdown_extensions:
  - attr_list
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - admonition
  - pymdownx.details
  - md_in_html
  - def_list
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      use_pygments: true
      pygments_lang_class: true
      auto_title: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.tasklist:
      custom_checkbox: true
      clickable_checkbox: false


plugins:
  - search
  - tags
  - git-revision-date-localized:
      enable_creation_date: true
      type: datetime
      enabled: true
      fallback_to_build_date: true
      locale: en


extra:
  tags:
    Homepage: homepage
    Index: index
    Overview: overview
    Test: test
    Infra: infra
    Documentation: doc
    Legal: legal
    User: user
    API: API
    Browser: browser

  status:
    new: Recently Added!


copyright: Only God knows

nav:
  - Homepage: index.md
  - {codebase_nav_path}:
    - main.py: main.py.md

"""

FILE_MARKDOWN: Final[str] = """# File: `{filename}`

Role: {role}

Path: `{file_path}`

{filedoc}

---

## Imports

{imports}

---

## Consts

{constants}

---

## Classes

{classes}

---

## Functions

{functions}

---

## Assertions

{assertions}
"""

IMPORT_MD_STRUCT: Final[str] = """### `#!py import {name}`

Path: `#!py {_path}`

Category: {category}

??? example "Snippet"

    ```py
{code}
    ```

"""

ASSIGN_MD_STRUCT: Final[str] = """### `#!py {token}`

Type: `#!py {_type}`

Value: `#!py {value}`

??? example "Snippet"

    ```py
{code}
    ```

"""

CLASS_DEF_MD_STRUCT: Final[str] = """### `#!py class {name}`

Parents: `{inheritance}`

Decorators: `#!py {decorators}`

Kwargs: `#!py {kwargs}`

??? quote "Docstring"

{docstring}

??? example "Snippet"

    ```py
{code}
    ```

"""

FUNCTION_DEF_MD_STRUCT: Final[str] = """### `#!py def {name}`

Type: `#!py {category}`

Return Type: `#!py {rtype}`

Decorators: `#!py {decorators}`

Args: `#!py {args}`

Kwargs: `#!py {kwargs}`

??? quote "Docstring"

{docstring}

??? example "Snippet"

    ```py
{code}
    ```

"""

ASSERT_MD_STRUCT: Final[str] = """### `#!py assert {test}`

Message: `#!py {msg}`

??? example "Snippet"

    ```py
{code}
    ```

"""
