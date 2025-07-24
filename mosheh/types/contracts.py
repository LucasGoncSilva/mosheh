"""
Thinking on security during runtime execution, specially for typing annotations and
standard contracts - since Python has not type checking it's strength - here are
defined the "Contracts" for each statement tracked.

These dataclasses are used to ensure the correct value type and attribution, so every
time each of them appears, they are going to have the desired and expected behavior.
"""

from dataclasses import asdict, dataclass
from typing import Any, Self

from mosheh.types.basic import (
    Annotation,
    Args,
    AssertionMessage,
    AssertionTest,
    CodeSnippet,
    Decorator,
    Docstring,
    ImportedIdentifier,
    Inheritance,
    Kwargs,
    ModuleName,
    ModulePath,
    Token,
    Value,
)
from mosheh.types.enums import FunctionType, ImportType, Statement


@dataclass
class BaseContract:
    """Base dataclass to shortcut `as_dict` definition."""

    @property
    def as_dict(self: Self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImportContract(BaseContract):
    """`ast.Import` contract for typing and declaration security."""

    statement: Statement
    name: ModuleName
    path: None
    category: ImportType
    code: CodeSnippet


@dataclass
class ImportFromContract(BaseContract):
    """`ast.ImportFrom` contract for typing and declaration security."""

    statement: Statement
    name: ImportedIdentifier
    path: ModulePath | None
    category: ImportType
    code: CodeSnippet


@dataclass
class AssignContract(BaseContract):
    """`ast.Assign` contract for typing and declaration security."""

    statement: Statement
    tokens: list[Token]
    value: Value
    code: CodeSnippet


@dataclass
class AnnAssignContract(BaseContract):
    """`ast.AnnAssign` contract for typing and declaration security."""

    statement: Statement
    name: Token
    annot: Annotation
    value: Value
    code: CodeSnippet


@dataclass
class FunctionDefContract(BaseContract):
    """`ast.FunctionDef` contract for typing and declaration security."""

    statement: Statement
    name: Token
    category: FunctionType
    docstring: Docstring | None
    decorators: list[Decorator]
    rtype: Annotation | None
    args: Args
    kwargs: Kwargs
    code: CodeSnippet


@dataclass
class AsyncFunctionDefContract(BaseContract):
    """`ast.AsyncFunctionDef` contract for typing and declaration security."""

    statement: Statement
    name: Token
    category: FunctionType
    docstring: Docstring | None
    decorators: list[Decorator]
    rtype: Annotation | None
    args: Args
    kwargs: Kwargs
    code: CodeSnippet


@dataclass
class ClassDefContract(BaseContract):
    """`ast.ClassDef` contract for typing and declaration security."""

    statement: Statement
    name: Token
    docstring: Docstring | None
    inheritance: list[Inheritance]
    decorators: list[Decorator]
    kwargs: Kwargs
    code: CodeSnippet


@dataclass
class AssertContract(BaseContract):
    """`ast.Assert` contract for typing and declaration security."""

    statement: Statement
    test: AssertionTest
    msg: AssertionMessage | None
    code: CodeSnippet
