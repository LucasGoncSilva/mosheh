# File: `custom_types.py`

Role: Python Source Code

Path: `mosheh`

For every type hint and annotation that goes beyond the traditional, there is a custom
type here created.

The idea of this types is to keep everything logical and short, with proper types and
in-code description. This is a way to turn Python into a "typed" lang, kinda.

The `Statement`, `ImportType`, `FunctionType` and `FileRole` classes are enums with a
really useful function: to standardize the possible types of their own types (for
example, a function strictly assumes only 4 different types, and exactly one of
them).

The other ones are `typing.TypeAlias`, simpler but also fuctional.

---

## Imports

### `#!py import Enum`

Path: `#!py enum`

Category: Native

??? example "Snippet"

    ```py
    from enum import Enum
    ```

### `#!py import auto`

Path: `#!py enum`

Category: Native

??? example "Snippet"

    ```py
    from enum import auto
    ```

### `#!py import TypeAlias`

Path: `#!py typing`

Category: Native

??? example "Snippet"

    ```py
    from typing import TypeAlias
    ```

---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class Statement`

Parents: `Enum`

Decorators: `#!py None`

Kwargs: `#!py None`

Enum-like class to enumerate in-code the dealed statements.

??? example "Snippet"

    ```py
    class Statement(Enum):
        """Enum-like class to enumerate in-code the dealed statements."""
        Import = auto()
        ImportFrom = auto()
        Assign = auto()
        AnnAssign = auto()
        ClassDef = auto()
        FunctionDef = auto()
        AsyncFunctionDef = auto()
        Assert = auto()
    ```

### `#!py class ImportType`

Parents: `Enum`

Decorators: `#!py None`

Kwargs: `#!py None`

Enum-like class to enumerate in-code the import types.

??? example "Snippet"

    ```py
    class ImportType(Enum):
        """Enum-like class to enumerate in-code the import types."""
        Native = 'Native'
        TrdParty = '3rd Party'
        Local = 'Local'
    ```

### `#!py class FunctionType`

Parents: `Enum`

Decorators: `#!py None`

Kwargs: `#!py None`

Enum-like class to enumerate in-code the function types.

??? example "Snippet"

    ```py
    class FunctionType(Enum):
        """Enum-like class to enumerate in-code the function types."""
        Function = 'Function'
        Method = 'Method'
        Generator = 'Generator'
        Coroutine = 'Coroutine'
    ```

### `#!py class FileRole`

Parents: `Enum`

Decorators: `#!py None`

Kwargs: `#!py None`

Enum-like class to enumerate in-code the files investigated.

??? example "Snippet"

    ```py
    class FileRole(Enum):
        """Enum-like class to enumerate in-code the files investigated."""
        PythonSourceCode = 'Python Source Code'
    ```

---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
