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

NodeHandlerDict: TypeAlias = (
    ImportHandlerDict
    | ImportFromHandlerDict
    | AssignHandlerDict
    | BinOpHandlerDict
    | AnnAssignHandlerDict
    | FunctionDefHandlerDict
)
