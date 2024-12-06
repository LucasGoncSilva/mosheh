# File: `custom_types.py`

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

??? example "SNIPPET"

    ```py
    class Statement(Enum):
        Import = auto()
        ImportFrom = auto()
        Assign = auto()
        AnnAssign = auto()
        ClassDef = auto()
        FunctionDef = auto()
        AsyncFunctionDef = auto()
        Assert = auto()
        BinOp = auto()
        Call = auto()
        Compare = auto()
        List = auto()
        Set = auto()
        Tuple = auto()
        Dict = auto()
        Slice = auto()
        Subscript = auto()
    ```

### `#!py class ImportType`

Parents: `Enum`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class ImportType(Enum):
        Native = 'Native'
        TrdParty = '3rd Party'
        Local = 'Local'
    ```

### `#!py class FunctionType`

Parents: `Enum`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class FunctionType(Enum):
        Function = 'Function'
        Method = 'Method'
        Generator = 'Generator'
        Coroutine = 'Coroutine'
    ```

---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
