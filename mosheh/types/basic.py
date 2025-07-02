from mosheh.types.enums import FileRole, FunctionType, ImportType, Statement


type Token = str
type ModuleName = str
type Notation = str
type Value = str
type DefaultValue = str
type FilePath = str
type ModulePath = str
type StatementName = str
type CodeSnippet = str
type Arg = str
type Kwarg = str
type AssertionTest = str
type AssertionMessage = str
type Docstring = str

type ImportedIdentifier = Token | ModuleName
type Decorator = Token | ModuleName
type Inheritance = Token | ModuleName
type ArgTuple = tuple[str, Notation | None, DefaultValue | None]

type StandardReturn = dict[
    str,
    Statement
    | ImportType
    | FunctionType
    | list[Decorator]
    | Inheritance
    | list[ArgTuple]
    | FileRole
    | None,
]


type StandardReturnProcessor = str | StandardReturn

type CodebaseDictValue = FilePath | StatementName

type CodebaseDict = dict[FilePath, list[StandardReturn]]
