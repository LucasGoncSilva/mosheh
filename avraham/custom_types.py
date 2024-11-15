from enum import Enum, auto
from typing import TypeAlias


class Statement(Enum):
    Import = auto()
    ImportFrom = auto()
    Assign = auto()
    AnnAssign = auto()
    FunctionDef = auto()
    AsyncFunctionDef = auto()
    ClassDef = auto()
    Assert = auto()
    BinOp = auto()
    Call = auto()
    Compare = auto()


class ImportType(Enum):
    Native = 'native'
    TrdParty = '3rd paty'
    Local = 'local'


Categorie: TypeAlias = dict[str, str]
ImportDict: TypeAlias = dict[str, ImportType | str | None]
ModuleDict: TypeAlias = dict[str, ImportDict]
ImportHandlerDict: TypeAlias = dict[str, Statement | ModuleDict]

ImportFromHandlerDict: TypeAlias = dict[str, Statement | list[str]]

CallHandlerDict: TypeAlias = dict[str, Statement | list[str]]

BinOpHandlerDict: TypeAlias = dict[str, Statement | str | CallHandlerDict]

AssignHandlerDict: TypeAlias = dict[str, Statement | list[str] | CallHandlerDict | str]

AnnAssignHandlerDict: TypeAlias = dict[str, Statement | str | CallHandlerDict]

FunctionDefHandlerDict: TypeAlias = dict[
    str, Statement | str | list[str] | CallHandlerDict | BinOpHandlerDict | None
]

AsyncFunctionDefHandlerDict: TypeAlias = dict[
    str, Statement | str | list[str] | CallHandlerDict | BinOpHandlerDict | None
]

ClassDefHandlerDict: TypeAlias = dict[
    str,
    Statement
    | str
    | list[str]
    | list[tuple]
    | CallHandlerDict
    | BinOpHandlerDict
    | None,
]

CompareHandlerDict: TypeAlias = dict[
    str, Statement | str | CallHandlerDict | list[str] | list[str | CallHandlerDict]
]

AssertHandlerDict: TypeAlias = dict[
    str, Statement | str | CompareHandlerDict | CallHandlerDict
]

NodeHandlerDict: TypeAlias = (
    ImportHandlerDict
    | ImportFromHandlerDict
    | AssignHandlerDict
    | BinOpHandlerDict
    | AnnAssignHandlerDict
    | FunctionDefHandlerDict
    | AsyncFunctionDefHandlerDict
    | ClassDefHandlerDict
    | CompareHandlerDict
    | AssertHandlerDict
)
