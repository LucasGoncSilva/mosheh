from mosheh.types.enums import FileRole, FunctionType, ImportType, Statement


def test_statement_enum() -> None:
    assert [
        'Import',
        'ImportFrom',
        'Assign',
        'AnnAssign',
        'ClassDef',
        'FunctionDef',
        'AsyncFunctionDef',
        'Assert',
    ] == [i.name for i in Statement]

    assert [
        'import',
        'importfrom',
        'assign',
        'annassign',
        'classdef',
        'functiondef',
        'asyncfunctiondef',
        'assert',
    ] == [i.value for i in Statement]


def test_import_type_enum() -> None:
    assert [
        'Native',
        'TrdParty',
        'Local',
    ] == [i.name for i in ImportType]

    assert [
        'native',
        'trdparty',
        'local',
    ] == [i.value for i in ImportType]


def test_function_type_enum() -> None:
    assert [
        'Function',
        'Method',
        'Generator',
        'Coroutine',
    ] == [i.name for i in FunctionType]

    assert [
        'function',
        'method',
        'generator',
        'coroutine',
    ] == [i.value for i in FunctionType]


def test_file_role_enum() -> None:
    assert [
        'PythonSourceCode',
        'PythonStubFile',
    ] == [i.name for i in FileRole]

    assert [
        ':material-language-python: Python Source Code',
        ':material-language-python: Python Stub File',
    ] == [i.value for i in FileRole]
