"""
Thinking on security during runtime execution, specially for typing annotations and
standard contracts - since Python has not type checking it's strength - here are
defined the "Contracts" for each statement tracked.

These dataclasses are used to ensure the correct value type and attribution, so every
time each of them appears, they are going to have the desired and expected behavior.
"""

from typing import NamedTuple

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


class ImportContract(NamedTuple):
    """`ast.Import` contract for typing and declaration security."""

    statement: Statement
    name: ModuleName
    path: None
    category: ImportType
    code: CodeSnippet


class ImportFromContract(NamedTuple):
    """`ast.ImportFrom` contract for typing and declaration security."""

    statement: Statement
    name: ImportedIdentifier
    path: ModulePath | None
    category: ImportType
    code: CodeSnippet


class AssignContract(NamedTuple):
    """`ast.Assign` contract for typing and declaration security."""

    statement: Statement
    tokens: list[Token]
    value: Value
    code: CodeSnippet


class AnnAssignContract(NamedTuple):
    """`ast.AnnAssign` contract for typing and declaration security."""

    statement: Statement
    name: Token
    annot: Annotation
    value: Value
    code: CodeSnippet


class FunctionDefContract(NamedTuple):
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


class AsyncFunctionDefContract(NamedTuple):
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


class ClassDefContract(NamedTuple):
    """`ast.ClassDef` contract for typing and declaration security."""

    statement: Statement
    name: Token
    docstring: Docstring | None
    inheritance: list[Inheritance]
    decorators: list[Decorator]
    kwargs: Kwargs
    code: CodeSnippet


class AssertContract(NamedTuple):
    """`ast.Assert` contract for typing and declaration security."""

    statement: Statement
    test: AssertionTest
    msg: AssertionMessage | None
    code: CodeSnippet
