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
