# File: `custom_types.py`

Role: Python Source Code

Path: `mosheh`

---

## Imports

### `#!py import Enum`

Path: `#!py enum`

Category: Native

??? example "SNIPPET"

    ```py
    from enum import Enum
    ```

### `#!py import auto`

Path: `#!py enum`

Category: Native

??? example "SNIPPET"

    ```py
    from enum import auto
    ```

### `#!py import TypeAlias`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

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

??? example "SNIPPET"

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

??? example "SNIPPET"

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

??? example "SNIPPET"

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

??? example "SNIPPET"

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
