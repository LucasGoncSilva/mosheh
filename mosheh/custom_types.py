"""
For every type hint and notation that goes beyond the traditional, there is a custom
type here created.

The idea of this types is to keep everything logical and short, with proper types and
in-code description. This is a way to turn Python into a "typed" lang, kinda.

The `Statement`, `ImportType`, `FunctionType` and `FileRole` classes are enums with a
really useful function: to standardize the possible types of their own types (for
example, a function strictly assumes only 4 different types, and exactly one of
them).

The other ones are `typing.TypeAlias`, simpler but also fuctional.
"""

# ruff: noqa

from enum import Enum, auto
from typing import TypeAlias


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


class ImportType(Enum):
    """Enum-like class to enumerate in-code the import types."""

    Native = 'Native'
    TrdParty = '3rd Party'
    Local = 'Local'


class FunctionType(Enum):
    """Enum-like class to enumerate in-code the function types."""

    Function = 'Function'
    Method = 'Method'
    Generator = 'Generator'
    Coroutine = 'Coroutine'


class FileRole(Enum):
    """Enum-like class to enumerate in-code the files investigated."""

    PythonSourceCode = 'Python Source Code'


Tokens: TypeAlias = list[str]
Decorators: TypeAlias = list[str]
Inheritance: TypeAlias = list[str]
ArgsKwargs: TypeAlias = list[tuple[str, str | None, str | None]]

StandardReturn: TypeAlias = dict[
    str,
    Statement
    | ImportType
    | FunctionType
    | FileRole
    | str
    | None
    | Tokens
    | Decorators
    | Inheritance
    | ArgsKwargs,
]

StandardReturnProcessor: TypeAlias = str | StandardReturn

CodebaseDict: TypeAlias = dict[str, list[StandardReturn]]
