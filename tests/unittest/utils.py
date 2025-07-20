from collections import defaultdict

from mosheh.types.basic import CodebaseDict, StandardReturn
from mosheh.utils import (
    add_to_nested_defaultdict,
    bin,
    convert_to_regular_dict,
    indent_code,
    is_lib_installed,
    nested_defaultdict,
    standard_struct,
)


def test_bin() -> None:
    assert bin(4, [1, 2, 3, 4, 5, 6, 7, 8])
    assert not bin(9, [1, 2, 3, 4, 5, 6, 7, 8])


def test_is_lib_installed() -> None:
    assert is_lib_installed('mosheh')
    assert not is_lib_installed('numpy')


def test_nested_defaultdict() -> None:
    assert isinstance(nested_defaultdict(), dict)
    assert isinstance(nested_defaultdict(), defaultdict)


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
    assert isinstance(standard_struct(), dict)
    assert not len(standard_struct())


def test_indent_code() -> None:
    code: str = 'def test_foo() -> None:\n    pass'
    result: str = indent_code(code)

    assert isinstance(result, str)
    assert result == '    def test_foo() -> None:\n        pass'
