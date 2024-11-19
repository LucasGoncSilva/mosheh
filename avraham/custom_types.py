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
    List = auto()
    Set = auto()
    Tuple = auto()
    Dict = auto()
    Slice = auto()
    Subscript = auto()


class ImportType(Enum):
    Native = 'native'
    TrdParty = '3rd paty'
    Local = 'local'


Categorie: TypeAlias = dict[str, str]
ImportDict: TypeAlias = dict[str, ImportType | str | None]
ModuleDict: TypeAlias = dict[str, ImportDict]
ImportHandlerDict: TypeAlias = dict[str, Statement | ModuleDict]

ImportFromHandlerDict: TypeAlias = dict[str, Statement | list[str]]

CallHandlerDict: TypeAlias = dict

BinOpHandlerDict: TypeAlias = dict

AssignHandlerDict: TypeAlias = dict

AnnAssignHandlerDict: TypeAlias = dict

FunctionDefHandlerDict: TypeAlias = dict

AsyncFunctionDefHandlerDict: TypeAlias = dict

ClassDefHandlerDict: TypeAlias = dict

CompareHandlerDict: TypeAlias = dict

AssertHandlerDict: TypeAlias = dict

ListHandlerDict: TypeAlias = dict

SetHandlerDict: TypeAlias = dict

TupleHandlerDict: TypeAlias = dict

DictHandlerDict: TypeAlias = dict

SliceHandlerDict: TypeAlias = dict

SubscriptHandlerDict: TypeAlias = dict

NodeHandler: TypeAlias = (
    str
    | dict[
        str,
        ImportHandlerDict
        | ImportFromHandlerDict
        | CallHandlerDict
        | BinOpHandlerDict
        | AssignHandlerDict
        | AnnAssignHandlerDict
        | FunctionDefHandlerDict
        | AsyncFunctionDefHandlerDict
        | ClassDefHandlerDict
        | CompareHandlerDict
        | AssertHandlerDict
        | ListHandlerDict
        | SetHandlerDict
        | TupleHandlerDict
        | DictHandlerDict
        | SliceHandlerDict
        | SubscriptHandlerDict,
    ]
)
