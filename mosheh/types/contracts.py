from dataclasses import asdict, dataclass
from typing import Any, Self

from mosheh.types.basic import (
    Arg,
    AssertionMessage,
    AssertionTest,
    CodeSnippet,
    Decorator,
    Docstring,
    ImportedIdentifier,
    Inheritance,
    Kwarg,
    ModuleName,
    ModulePath,
    Notation,
    Token,
    Value,
)
from mosheh.types.enums import FunctionType, ImportType, Statement


@dataclass
class BaseContract:
    @property
    def as_dict(self: Self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImportContract(BaseContract):
    statement: Statement
    name: ModuleName
    path: None
    category: ImportType
    code: CodeSnippet


@dataclass
class ImportFromContract(BaseContract):
    statement: Statement
    name: ImportedIdentifier
    path: ModulePath | None
    category: ImportType
    code: CodeSnippet


@dataclass
class AssignContract(BaseContract):
    statement: Statement
    tokens: list[Token]
    value: Value
    code: CodeSnippet


@dataclass
class AnnAssignContract(BaseContract):
    statement: Statement
    name: Token
    annot: Notation
    value: Value
    code: CodeSnippet


@dataclass
class FunctionDefContract(BaseContract):
    statement: Statement
    name: Token
    category: FunctionType
    docstring: Docstring | None
    decorators: list[Decorator]
    rtype: Notation | None
    args: Arg
    kwargs: Kwarg
    code: CodeSnippet


@dataclass
class AsyncFunctionDefContract(BaseContract):
    statement: Statement
    name: Token
    category: FunctionType
    docstring: Docstring | None
    decorators: list[Decorator]
    rtype: Notation | None
    args: Arg
    kwargs: Kwarg
    code: CodeSnippet


@dataclass
class ClassDefContract(BaseContract):
    statement: Statement
    name: Token
    docstring: Docstring | None
    inheritance: list[Inheritance]
    decorators: list[Decorator]
    kwargs: Kwarg
    code: CodeSnippet


@dataclass
class AssertContract(BaseContract):
    statement: Statement
    test: AssertionTest
    msg: AssertionMessage | None
    code: CodeSnippet
