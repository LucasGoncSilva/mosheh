from collections import defaultdict
from typing import Any

from hypothesis import given as g
from hypothesis import strategies as st

from mosheh.types.basic import CodebaseDict, StandardReturn
from mosheh.types.enums import ImportType
from mosheh.utils import (
    add_to_nested_defaultdict,
    bin,
    convert_to_regular_dict,
    get_import_type,
    indent_code,
    nested_defaultdict,
    standard_struct,
)


@g(st.lists(st.integers(), min_size=1).map(sorted))
def test_bin(data: list[int]) -> None:
    assert bin(data[0], data)


def test_get_import_type() -> None:
    assert get_import_type('os') == ImportType.Native
    assert get_import_type('stdlib_list') == ImportType.TrdParty


def test_nested_defaultdict() -> None:
    dct: defaultdict[Any, Any] = nested_defaultdict()

    assert isinstance(dct, dict)
    assert isinstance(dct, defaultdict)


def test_add_to_nested_defaultdict() -> None:
    structure: defaultdict[str, dict[str, dict[str, list[dict[str, str]]]]] = (
        nested_defaultdict()
    )
    path: list[str] = ['level1', 'level2', 'level3']
    data: list[StandardReturn] = [{'key': 'value'}]

    result: defaultdict[str, dict[str, dict[str, list[dict[str, str]]]]] = (
        add_to_nested_defaultdict(structure, path, data)
    )

    assert isinstance(result, dict)
    assert isinstance(result, defaultdict)
    assert result == defaultdict(
        defaultdict, {'level1': {'level2': {'level3': [{'key': 'value'}]}}}
    )


def test_convert_to_regular_dict() -> None:
    structure: defaultdict[str, str] = nested_defaultdict()
    added: defaultdict[str, str] = add_to_nested_defaultdict(
        structure, ['level1'], [{'key': 'value'}]
    )
    result: CodebaseDict = convert_to_regular_dict(added)

    assert isinstance(result, dict)
    assert not isinstance(result, defaultdict)
    assert result == {'level1': [{'key': 'value'}]}


def test_standard_struct() -> None:
    dct: dict[Any, Any] = standard_struct()

    assert isinstance(dct, dict)
    assert not len(dct)


def test_indent_code() -> None:
    code: str = 'def test_foo() -> None:\n    pass'
    result: str = indent_code(code)

    assert isinstance(result, str)
    assert result == '    def test_foo() -> None:\n        pass'
