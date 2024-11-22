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
    Native = 'Native'
    TrdParty = '3rd Party'
    Local = 'Local'


class Lang(Enum):
    PT_BR = 'pt-BR'
    EN = 'en'


Categorie: TypeAlias = dict[str, str]
ImportDict: TypeAlias = dict[str, ImportType | str | None]
ModuleDict: TypeAlias = dict[str, ImportDict]

ImportHandlerDict: TypeAlias = dict[str, Statement | ModuleDict]

ImportFromHandlerDict: TypeAlias = dict[
    str, Statement | ImportType | list[str] | str | None
]

AssignHandlerDict: TypeAlias = dict[str, Statement | str | list[str]]

CallHandlerDict: TypeAlias = dict[str, Statement | str | list[str]]

ClassDefHandlerDict: TypeAlias = dict[
    str, Statement | str | list[str] | list[tuple[str, str]]
]

CompareHandlerDict: TypeAlias = dict[
    str, Statement | str | CallHandlerDict | list[str] | list[CallHandlerDict | str]
]

AssertTest: TypeAlias = CompareHandlerDict | str
AssertHandlerDict: TypeAlias = dict[str, Statement | str | AssertTest | None]

DictHandlerDict: TypeAlias = dict[str, Statement | list[str]]

ArgList: TypeAlias = list[tuple[str, str | None, str | CallHandlerDict | None]]
FunctionDefHandlerDict: TypeAlias = dict[
    str, Statement | str | list[str] | ArgList | None
]

AsyncFunctionDefHandlerDict: TypeAlias = dict[
    str, Statement | str | list[str] | ArgList | None
]

_SetHandlerDict: TypeAlias = dict[str, Statement]

SliceHandlerDict: TypeAlias = dict[str, Statement | str]

SubscriptHandlerDict: TypeAlias = dict[str, Statement | str | SliceHandlerDict]

_ListItem: TypeAlias = CallHandlerDict | str | dict[str, Statement | str]
_ListHandlerDict: TypeAlias = dict[str, Statement | list[_ListItem]]

_TupleHandlerDict: TypeAlias = dict[str, Statement | list[_ListItem]]

AnnAssignValue: TypeAlias = str | CallHandlerDict
AnnAssignHandlerDict: TypeAlias = dict[str, Statement | str | AnnAssignValue]

BinOperand: TypeAlias = (
    str
    | CallHandlerDict
    | _ListHandlerDict
    | _SetHandlerDict
    | DictHandlerDict
    | _TupleHandlerDict
)
BinOpHandlerDict: TypeAlias = dict[str, Statement | str | BinOperand]

ListItem: TypeAlias = CallHandlerDict | str | BinOpHandlerDict
ListHandlerDict: TypeAlias = dict[str, Statement | list[ListItem]]
TupleHandlerDict: TypeAlias = dict[str, Statement | list[ListItem]]
SetHandlerDict: TypeAlias = dict[str, Statement | list[ListItem]]

NodeHandler: TypeAlias = (
    str
    | ImportHandlerDict
    | BinOperand
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
    | SubscriptHandlerDict
)

CodebaseDict: TypeAlias = dict[str, list[NodeHandler]]
