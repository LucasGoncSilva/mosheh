from hypothesis import given as g
from hypothesis import strategies as st

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


@g(st.characters(), st.characters())
def test_import_contract(name: str, code: str) -> None:
    contract: ImportContract = ImportContract(
        statement=Statement.Import,
        name=name,
        path=None,
        category=ImportType.Native,
        code=code,
    )

    expected: dict[str, str | Statement | ImportType | None] = {
        'statement': Statement.Import,
        'name': name,
        'path': None,
        'category': ImportType.Native,
        'code': code,
    }

    assert isinstance(contract, ImportContract)
    assert contract._asdict() == expected


@g(st.characters(), st.characters(), st.characters())
def test_import_from_contract(name: str, path: str, code: str) -> None:
    contract: ImportFromContract = ImportFromContract(
        statement=Statement.ImportFrom,
        name=name,
        path=path,
        category=ImportType.Native,
        code=code,
    )

    expected: dict[str, str | Statement | ImportType] = {
        'statement': Statement.ImportFrom,
        'name': name,
        'path': path,
        'category': ImportType.Native,
        'code': code,
    }

    assert isinstance(contract, ImportFromContract)
    assert contract._asdict() == expected


@g(st.lists(st.characters(), min_size=1), st.characters(), st.characters())
def test_assign_contract(tokens: list[str], value: str, code: str) -> None:
    contract: AssignContract = AssignContract(
        statement=Statement.Assign, tokens=tokens, value=value, code=code
    )

    expected: dict[str, str | Statement | list[str]] = {
        'statement': Statement.Assign,
        'tokens': tokens,
        'value': value,
        'code': code,
    }

    assert isinstance(contract, AssignContract)
    assert contract._asdict() == expected


@g(st.characters(), st.characters(), st.characters(), st.characters())
def test_ann_assign_contract(name: str, annot: str, value: str, code: str) -> None:
    contract: AnnAssignContract = AnnAssignContract(
        statement=Statement.AnnAssign,
        name=name,
        annot=annot,
        value=value,
        code=code,
    )

    expected: dict[str, str | Statement] = {
        'statement': Statement.AnnAssign,
        'name': name,
        'annot': annot,
        'value': value,
        'code': code,
    }

    assert isinstance(contract, AnnAssignContract)
    assert contract._asdict() == expected


@g(
    st.characters(),
    st.characters() | st.none(),
    st.lists(st.characters()),
    st.lists(st.characters()),
    st.characters(),
    st.characters(),
)
def test_class_contract(
    name: str,
    docstring: str | None,
    decorators: list[str],
    inheritance: list[str],
    kwargs: str,
    code: str,
) -> None:
    contract: ClassDefContract = ClassDefContract(
        statement=Statement.ClassDef,
        name=name,
        docstring=docstring,
        decorators=decorators,
        inheritance=inheritance,
        kwargs=kwargs,
        code=code,
    )

    expected: dict[str, str | Statement | None | list[str]] = {
        'statement': Statement.ClassDef,
        'name': name,
        'docstring': docstring,
        'decorators': decorators,
        'inheritance': inheritance,
        'kwargs': kwargs,
        'code': code,
    }

    assert isinstance(contract, ClassDefContract)
    assert contract._asdict() == expected


@g(
    st.characters(),
    st.characters(),
    st.characters(),
    st.lists(st.characters()),
    st.characters() | st.none(),
    st.characters(),
    st.characters(),
)
def test_function_contract(
    name: str,
    args: str,
    kwargs: str,
    decorators: list[str],
    docstring: str | None,
    rtype: str,
    code: str,
) -> None:
    contract: FunctionDefContract = FunctionDefContract(
        statement=Statement.FunctionDef,
        category=FunctionType.Function,
        name=name,
        args=args,
        kwargs=kwargs,
        decorators=decorators,
        docstring=docstring,
        rtype=rtype,
        code=code,
    )

    expected: dict[str, str | Statement | FunctionType | list[str] | None] = {
        'statement': Statement.FunctionDef,
        'category': FunctionType.Function,
        'name': name,
        'args': args,
        'kwargs': kwargs,
        'decorators': decorators,
        'docstring': docstring,
        'rtype': rtype,
        'code': code,
    }

    assert isinstance(contract, FunctionDefContract)
    assert contract._asdict() == expected


@g(
    st.characters(),
    st.characters(),
    st.characters(),
    st.lists(st.characters()),
    st.characters() | st.none(),
    st.characters(),
    st.characters(),
)
def test_async_function_contract(
    name: str,
    args: str,
    kwargs: str,
    decorators: list[str],
    docstring: str | None,
    rtype: str,
    code: str,
) -> None:
    contract: FunctionDefContract = FunctionDefContract(
        statement=Statement.AsyncFunctionDef,
        category=FunctionType.Method,
        name=name,
        args=args,
        kwargs=kwargs,
        decorators=decorators,
        docstring=docstring,
        rtype=rtype,
        code=code,
    )

    expected: dict[str, str | Statement | FunctionType | list[str] | None] = {
        'statement': Statement.AsyncFunctionDef,
        'category': FunctionType.Method,
        'name': name,
        'args': args,
        'kwargs': kwargs,
        'decorators': decorators,
        'docstring': docstring,
        'rtype': rtype,
        'code': code,
    }

    assert isinstance(contract, FunctionDefContract)
    assert contract._asdict() == expected


@g(st.characters(), st.characters() | st.none(), st.characters())
def test_assert_contract(test: str, msg: str | None, code: str) -> None:
    contract: AssertContract = AssertContract(
        statement=Statement.Assert, test=test, msg=msg, code=code
    )

    expected: dict[str, str | Statement | None] = {
        'statement': Statement.Assert,
        'test': test,
        'msg': msg,
        'code': code,
    }

    assert isinstance(contract, AssertContract)
    assert contract._asdict() == expected
