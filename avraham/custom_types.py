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