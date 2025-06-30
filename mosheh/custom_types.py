"""
For every type hint and notation that goes beyond the traditional, there is a custom
type here created.

The idea of this types is to keep everything logical and short, with proper types and
in-code description. This is a way to turn Python into a "typed" lang, kinda.

The `Statement`, `ImportType`, `FunctionType` and `FileRole` classes are strenums with a
really useful function: to standardize the possible types of their own types (for
example, a function strictly assumes only 4 different types, and exactly one of
them).

The other ones are common `type` definitions, simpler but also useful.
"""

from enum import StrEnum, auto


class Statement(StrEnum):
    """Enum-like class to enumerate in-code the dealed statements."""

    Import = auto()
    ImportFrom = auto()
    Assign = auto()
    AnnAssign = auto()
    ClassDef = auto()
    FunctionDef = auto()
    AsyncFunctionDef = auto()
    Assert = auto()


class ImportType(StrEnum):
    """Enum-like class to enumerate in-code the import types."""

    Native = auto()
    TrdParty = auto()
    Local = auto()


class FunctionType(StrEnum):
    """Enum-like class to enumerate in-code the function types."""

    Function = auto()
    Method = auto()
    Generator = auto()
    Coroutine = auto()


class FileRole(StrEnum):
    """Enum-like class to enumerate in-code the files investigated."""

    PythonSourceCode = auto()


type Token = str
type Notation = str
type DefaultValue = str

type Decorator = Token
type Inheritance = Token
type ArgKwarg = tuple[str, Notation | None, DefaultValue | None]

type Decorators = list[Decorator]
type ArgsKwargs = list[ArgKwarg]

type Tokens = list[Token | Decorator | Inheritance]

type StandardReturn = dict[
    str,
    Statement
    | ImportType
    | FunctionType
    | FileRole
    | str
    | Tokens
    | Decorators
    | Inheritance
    | ArgsKwargs
    | None,
]

type StandardReturnProcessor = str | StandardReturn

type CodebaseDict = dict[str, list[StandardReturn]]
