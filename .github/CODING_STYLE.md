# Coding Style

> In Mosheh, consistency is essential. This guide outlines the Python conventions we follow: PEP-aligned, type-safe, readable, and testable. Clean code comes first; style is automated.

## General Principles

- Adhere to [PEP 8](https://peps.python.org/pep-0008/) and [PEP 484/561](https://peps.python.org/pep-0484/) for typing.
- Code **must explain itself**. Comments are allowed only when clarity can’t be improved otherwise.
- Always follow the existing style of the file you modify—even if it slightly diverges from standards.
- Prefer explicit, readable patterns over clever but obscure code.

## Formatting & Linting

We use **Ruff** and **mypy** to enforce formatting, lint rules, and type safety.

Run before committing:

```sh
uv run task lint
```

All reported issues must be resolved before merging.

### Ruﬀ Configuration Highlights

- Single quotes by default
- Line length: 88 characters
- 2 blank lines after import block
- Import ordering: std -> third-party -> local
- Ruff doesn’t enforce PascalCase for classes; reviewers may request adjustments.

## Naming Conventions

| Entity            | Style                | Example                         |
| ----------------- | -------------------- | ------------------------------- |
| Simple Variables  | snake_case           | `simple_timeout: [type] = ...`  |
| Constants         | UPPER_SNAKE_CASE     | `DEFAULT_TIMEOUT: [type] = ...` |
| Functions/Methods | snake_case           | `def render_docs()`             |
| Classes           | PascalCase           | `class DocumentBuilder`         |
| Private Members   | \_leading_underscore | `def _internal_method()`        |
| Type Aliases      | PascalCase           | `type FilePath = str`           |

## Type Annotations

- Variables, functions and methods, as all as possible, **must** have type annotations.
- Use `mypy` with `strict = true`; fix all type issues.
- Avoid `Any` unless explicitly justified.
- Prefer clear naming or comments over complex casts.

## Private Members

- Prefix any private function/method/variable with a single underscore (`_`).
- Private elements must **not** be used outside their intended scope.
- If you need broader access, make it public and add proper docstrings.

## Comments & Docstrings

**Always** include a module-level docstring at the top of every `.py` file.

Example from `constants.py`:

```py
"""
This module defines constants and templates used throughout the project.

It aims to standardize project-wide values, ensure consistency, and streamline the
development and documentation process.

...
"""
```

### Function/method docstrings

Use the following style—with a one-line summary, blank line, details, and Sphinx-style `:param:`/`:type:`/`:returns:`/`:rtype:` sections:

```py
def set_logging_config(v: int = 3) -> None:
    """
    Configures the logging level for the application based on the provided verbosity.

    Logging is handled using `RichHandler` for enhanced terminal output. The verbosity
    level `v` controls the logging granularity for the `mosheh` logger, and optionally
    for the `mkdocs` logger in debug mode.

    :param v: Verbosity level, from 0 (critical) to 4 (debug). Defaults to 3 (info).
        - 0: Critical
        - 1: Error
        - 2: Warning
        - 3: Info (default)
        - 4: Debug
    :type v: int
    :returns: None.
    :rtype: None
    """
    ...
```

- The first line is a summary.
- Leave a blank line, then provide details or notes.
- Use `:param:`, `:type:`, `:returns:`, `:rtype:` — do not include `:raises:` unless warranted.
- Avoid redundant comments that restate obvious code.

## Testing

- Code changes must include or update **pytest** tests (in `tests/unittest/`).
- Use descriptive test names and avoid relying on docstrings alone.
- Run both unit and documentation CLI tests:

```sh
uv run task test
```

## Pre-Merge Checklist

Before your PR, ensure:

- [x] Style and naming follow conventions
- [x] `uv run task lint` yields zero issues (runs 2x if needed)
- [x] `uv run task test` passes
- [x] All files start with meaningful module docstrings
- [x] No debug prints or commented-out code remain
- [x] Docstrings accurately describe each public API

## When in Doubt

- Match the style of existing code.
- Ask in GitHub if unsure about introducing new patterns.
- Clarity beats cleverness—always.
