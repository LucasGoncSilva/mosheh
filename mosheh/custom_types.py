from enum import Enum, auto
from typing import TypeAlias, Final


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


class Lang(Enum):
    PT_BR = 'pt-BR'
    EN = 'en'


Categorie: TypeAlias = Final[dict[str, str]]
ImportDict: TypeAlias = Final[dict[str, ImportType | str | None]]
ModuleDict: TypeAlias = Final[dict[str, ImportDict]]

ImportHandlerDict: TypeAlias = Final[dict[str, Statement | ModuleDict]]

ImportFromHandlerDict: TypeAlias = Final[
    dict[str, Statement | ImportType | list[str] | str | None]
]

AssignHandlerDict: TypeAlias = Final[dict[str, Statement | str | list[str]]]

CallHandlerDict: TypeAlias = Final[dict[str, Statement | str | list[str]]]

ClassDefHandlerDict: TypeAlias = Final[
    dict[str, Statement | str | list[str] | list[tuple[str, str]]]
]

CompareHandlerDict: TypeAlias = Final[
    dict[
        str, Statement | str | CallHandlerDict | list[str] | list[CallHandlerDict | str]
    ]
]

AssertTest: TypeAlias = Final[CompareHandlerDict | str]
AssertHandlerDict: TypeAlias = Final[dict[str, Statement | str | AssertTest | None]]

DictHandlerDict: TypeAlias = Final[dict[str, Statement | list[str]]]

ArgList: TypeAlias = Final[list[tuple[str, str | None, str | CallHandlerDict | None]]]
FunctionDefHandlerDict: TypeAlias = Final[
    dict[str, Statement | str | list[str] | ArgList | None]
]
AsyncFunctionDefHandlerDict: TypeAlias = Final[
    dict[str, Statement | str | list[str] | ArgList | None]
]

_SetHandlerDict: TypeAlias = Final[dict[str, Statement]]

SliceHandlerDict: TypeAlias = Final[dict[str, Statement | str]]

SubscriptHandlerDict: TypeAlias = Final[dict[str, Statement | str | SliceHandlerDict]]

_ListItem: TypeAlias = Final[CallHandlerDict | str | dict[str, Statement | str]]
_ListHandlerDict: TypeAlias = Final[dict[str, Statement | list[_ListItem]]]

_TupleHandlerDict: TypeAlias = Final[dict[str, Statement | list[_ListItem]]]

AnnAssignValue: TypeAlias = Final[str | CallHandlerDict]
AnnAssignHandlerDict: TypeAlias = Final[dict[str, Statement | str | AnnAssignValue]]

BinOperand: TypeAlias = (
    str
    | CallHandlerDict
    | _ListHandlerDict
    | _SetHandlerDict
    | DictHandlerDict
    | _TupleHandlerDict
)
BinOpHandlerDict: TypeAlias = Final[dict[str, Statement | str | BinOperand]]

ListItem: TypeAlias = Final[CallHandlerDict | str | BinOpHandlerDict]
ListHandlerDict: TypeAlias = Final[dict[str, Statement | list[ListItem]]]
TupleHandlerDict: TypeAlias = Final[dict[str, Statement | list[ListItem]]]
SetHandlerDict: TypeAlias = Final[dict[str, Statement | list[ListItem]]]

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

CodebaseDict: TypeAlias = Final[dict[str, list[NodeHandler]]]
