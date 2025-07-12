"""
Not a secret about these definitions, it's as simple as possible.

The idea here is not to create custom complex types, but to serve as hints about
what shoud be here or there; most of the type aliases are just commom strings, but
their names helps when reading a long, deeper code, showing if that string should
be an argument or a code snippet.

The use of `typing.Annotated` does not change the alias itself, but helps with a
description about the type.
"""

from typing import Annotated

from mosheh.types.enums import FileRole, FunctionType, ImportType, Statement


type Token = Annotated[str, 'Variable, function or parameter name']
type ModuleName = Annotated[str, 'Imported module name']
type Notation = Annotated[str, 'Typing notation']
type Value = Annotated[str, 'Variable assigned value']
type DefaultValue = Annotated[str, 'Default value']
type FilePath = Annotated[str, 'File or dir name']
type ModulePath = Annotated[str, 'Path for a module import']
type CodeSnippet = Annotated[str, 'Code snippet, example']
type Args = Annotated[str, 'Arguments (e.g. `name: type = default`)']
type Kwargs = Annotated[str, 'Arguments (e.g. `name: type = default`)']
type AssertionTest = Annotated[str, 'Assertion itself']
type AssertionMessage = Annotated[str, 'Assertion return message']
type Docstring = Annotated[str, 'Class or function docstring']

type ImportedIdentifier = Annotated[Token | ModuleName, 'Importable stuff']
type Decorator = Annotated[Token | ModuleName, 'Class or func decorator']
type Inheritance = Annotated[Token | ModuleName, 'Classes which a class inherits']

type StandardReturn = dict[
    str,
    Statement
    | ImportType
    | FunctionType
    | list[Decorator]
    | Inheritance
    | FileRole
    | None,
]


type StandardReturnProcessor = str | StandardReturn

type CodebaseDict = dict[FilePath, list[StandardReturn]]
