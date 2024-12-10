from collections import defaultdict

from mosheh.custom_types import StandardReturn
from mosheh.utils import (
    add_to_dict,
    bin,
    convert_to_regular_dict,
    indent_code,
    is_lib_installed,
    nested_dict,
    standard_struct,
)


def test_bin():
    assert bin(4, [1, 2, 3, 4, 5, 6, 7, 8])
    assert not bin(9, [1, 2, 3, 4, 5, 6, 7, 8])


def test_is_lib_installed():
    assert is_lib_installed('mosheh')
    assert not is_lib_installed('numpy')


def test_nested_dict():
    assert isinstance(nested_dict(), dict)
    assert isinstance(nested_dict(), defaultdict)


def test_add_to_dict():
    structure: defaultdict[str, str] = nested_dict()
    path: list[str] = ['level1', 'level2', 'level3']
    data: list[StandardReturn] = [{'key': 'value'}]

    result: defaultdict[str, str | defaultdict[str, str]] = add_to_dict(
        structure, path, data
    )

    assert isinstance(result, dict)
    assert isinstance(result, defaultdict)
    assert result == defaultdict(
        defaultdict, {'level1': {'level2': {'level3': [{'key': 'value'}]}}}
    )


def test_convert_to_regular_dict():
    structure: defaultdict[str, str] = nested_dict()
    added: defaultdict[str, str] = add_to_dict(
        structure, ['level1'], [{'key': 'value'}]
    )
    result: dict[str, dict[str, str]] = convert_to_regular_dict(added)

    assert isinstance(result, dict)
    assert not isinstance(result, defaultdict)
    assert result == {'level1': [{'key': 'value'}]}


def test_standard_struct():
    assert isinstance(standard_struct(), dict)
    assert not len(standard_struct())


def test_indent_code():
    code: str = 'def test_foo() -> None:\n    pass'
    result: str = indent_code(code)

    assert isinstance(result, str)
    assert result == '    def test_foo() -> None:\n        pass'
