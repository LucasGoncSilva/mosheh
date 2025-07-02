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

    PythonSourceCode = ':material-language-python: Python Source Code'
