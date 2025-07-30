from mosheh.types.contracts import (
    AnnAssignContract,
    AssertContract,
    AssignContract,
    ClassDefContract,
    FunctionDefContract,
    ImportContract,
    ImportFromContract,
)
from mosheh.types.enums import FunctionType, ImportType, Statement


def test_import_contract() -> None:
    contract: ImportContract = ImportContract(
        statement=Statement.Import,
        name='os',
        path=None,
        category=ImportType.Native,
        code='import os',
    )

    expected: dict[str, str | Statement | ImportType | None] = {
        'statement': Statement.Import,
        'name': 'os',
        'path': None,
        'category': ImportType.Native,
        'code': 'import os',
    }

    assert isinstance(contract, ImportContract)
    assert contract._asdict() == expected


def test_import_from_contract() -> None:
    contract: ImportFromContract = ImportFromContract(
        statement=Statement.ImportFrom,
        name='mean',
        path='math',
        category=ImportType.Native,
        code='from math import mean',
    )

    expected: dict[str, str | Statement | ImportType] = {
        'statement': Statement.ImportFrom,
        'name': 'mean',
        'path': 'math',
        'category': ImportType.Native,
        'code': 'from math import mean',
    }

    assert isinstance(contract, ImportFromContract)
    assert contract._asdict() == expected


def test_assign_contract() -> None:
    contract: AssignContract = AssignContract(
        statement=Statement.Assign, tokens=['FOO'], value='123', code='FOO = 123'
    )

    expected: dict[str, str | Statement | list[str]] = {
        'statement': Statement.Assign,
        'tokens': ['FOO'],
        'value': '123',
        'code': 'FOO = 123',
    }

    assert isinstance(contract, AssignContract)
    assert contract._asdict() == expected


def test_ann_assign_contract() -> None:
    contract: AnnAssignContract = AnnAssignContract(
        statement=Statement.AnnAssign,
        name='NUM',
        annot='Final[int]',
        value='404',
        code='NUM: Final[int] = 404',
    )

    expected: dict[str, str | Statement] = {
        'statement': Statement.AnnAssign,
        'name': 'NUM',
        'annot': 'Final[int]',
        'value': '404',
        'code': 'NUM: Final[int] = 404',
    }

    assert isinstance(contract, AnnAssignContract)
    assert contract._asdict() == expected


def test_class_contract() -> None:
    contract: ClassDefContract = ClassDefContract(
        statement=Statement.ClassDef,
        name='Example',
        docstring=None,
        decorators=[],
        inheritance=['@dataclass'],
        kwargs='',
        code='@dataclass\nclass Example:',
    )

    expected: dict[str, str | Statement | None | list[str]] = {
        'statement': Statement.ClassDef,
        'name': 'Example',
        'docstring': None,
        'decorators': [],
        'inheritance': ['@dataclass'],
        'kwargs': '',
        'code': '@dataclass\nclass Example:',
    }

    assert isinstance(contract, ClassDefContract)
    assert contract._asdict() == expected


def test_function_contract() -> None:
    contract: FunctionDefContract = FunctionDefContract(
        statement=Statement.FunctionDef,
        category=FunctionType.Function,
        name='sum_2',
        args='x: int',
        kwargs='',
        decorators=[],
        docstring=None,
        rtype='int',
        code='def sum_2(x: int) -> int:',
    )

    expected: dict[str, str | Statement | FunctionType | list[str] | None] = {
        'statement': Statement.FunctionDef,
        'category': FunctionType.Function,
        'name': 'sum_2',
        'args': 'x: int',
        'kwargs': '',
        'decorators': [],
        'docstring': None,
        'rtype': 'int',
        'code': 'def sum_2(x: int) -> int:',
    }

    assert isinstance(contract, FunctionDefContract)
    assert contract._asdict() == expected


def test_async_function_contract() -> None:
    contract: FunctionDefContract = FunctionDefContract(
        statement=Statement.AsyncFunctionDef,
        category=FunctionType.Method,
        name='sum_2',
        args='x: int',
        kwargs='',
        decorators=[],
        docstring=None,
        rtype='int',
        code='async def sum_2(x: int) -> int:',
    )

    expected: dict[str, str | Statement | FunctionType | list[str] | None] = {
        'statement': Statement.AsyncFunctionDef,
        'category': FunctionType.Method,
        'name': 'sum_2',
        'args': 'x: int',
        'kwargs': '',
        'decorators': [],
        'docstring': None,
        'rtype': 'int',
        'code': 'async def sum_2(x: int) -> int:',
    }

    assert isinstance(contract, FunctionDefContract)
    assert contract._asdict() == expected


def test_assert_contract() -> None:
    contract: AssertContract = AssertContract(
        statement=Statement.Assert, test='1 == 1', msg=None, code='assert 1 == 1'
    )

    expected: dict[str, str | Statement | None] = {
        'statement': Statement.Assert,
        'test': '1 == 1',
        'msg': None,
        'code': 'assert 1 == 1',
    }

    assert isinstance(contract, AssertContract)
    assert contract._asdict() == expected
