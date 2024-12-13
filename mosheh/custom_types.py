# ruff: noqa

from enum import Enum, auto
from typing import TypeAlias


class Statement(Enum):
    Import = auto()
    ImportFrom = auto()
    Assign = auto()
    AnnAssign = auto()
    ClassDef = auto()
    FunctionDef = auto()
    AsyncFunctionDef = auto()
    Assert = auto()


class ImportType(Enum):
    Native = 'Native'
    TrdParty = '3rd Party'
    Local = 'Local'


class FunctionType(Enum):
    Function = 'Function'
    Method = 'Method'
    Generator = 'Generator'
    Coroutine = 'Coroutine'


Tokens: TypeAlias = list[str]
Decorators: TypeAlias = list[str]
Inheritance: TypeAlias = list[str]
ArgsKwargs: TypeAlias = list[tuple[str, str | None, str | None]]

StandardReturn: TypeAlias = dict[
    str,
    Statement
    | ImportType
    | FunctionType
    | str
    | None
    | Tokens
    | Decorators
    | Inheritance
    | ArgsKwargs,
]

StandardReturnProcessor: TypeAlias = str | StandardReturn

CodebaseDict: TypeAlias = dict[str, list[StandardReturn]]
