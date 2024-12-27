from collections import defaultdict
from collections.abc import Sequence
from copy import deepcopy
from importlib.util import find_spec
from typing import Any

from .custom_types import StandardReturn


def bin(item: Any, universe: Sequence[Any]) -> bool:
    """
    Binary Search algorithm which returns not the index, but a boolean.

    It inicializes two "pointers", one for the low or start of the iterator
    and another for the high or the end of it. Gets the middle point and
    compares it with the asked item.

    If the item is greater/after the middle the middle becomes the new low
    and repeats, otherwise, it becomes the new high and so on and so on and
    so on... until the item is found and returns True or not, returning False.

    Example:
    ```python
    lst: list[int] = [1, 2, 3, 4, 5]
    num: int = 4
    bin(num, lst)
    # True
    ```

    :param item: The item to check if exists in.
    :type item: Any
    :param universe: The sorted iterable to be evaluated.
    :type universe: Sequence[Any]
    :return: If the item is found in the universe.
    :rtype: bool
    """

    low: int = 0
    high: int = len(universe) - 1
    mid: int = 0

    while low <= high:
        mid = (high + low) // 2

        if universe[mid] < item:
            low = mid + 1
        elif universe[mid] > item:
            high = mid - 1
        else:
            return True

    return False


def is_lib_installed(name: str) -> bool:
    """
    Checks if a lib exists in the environment path.

    By literally just... find spec using... unhh... find_spec()... searches
    for modules in the environment path and returns it.

    Example:
    ```python
    is_lib_installed('fastapi')
    # False
    ```

    :param name: The name of the lib, e.g. numpy or numba.
    :type name: str
    :return: Whether the lib exists in the env.
    :rtype: bool
    """

    try:
        return True if find_spec(name) is not None else False
    except (ModuleNotFoundError, ValueError):
        return False


def nested_dict() -> defaultdict[Any, Any]:
    """
    Creates and returns a nested dictionary using `collections.defaultdict`.

    This function generates a `defaultdict` where each key defaults to another
    `nested_dict`, allowing the creation of arbitrarily deep dictionaries without
    needing to explicitly define each level.

    Key concepts:
    - defaultdict: A specialized dictionary from the `collections` module
      that automatically assigns a default value for missing keys. In this case, the
      default value is another `nested_dict`, enabling recursive dictionary nesting.

    Example:
    ```python
    d = nested_dict()
    d['level1']['level2']['level3'] = 'text'
    # {'level': {'level2': {'level3': 'text'}}}
    ```

    :return: A `defaultdict` instance configured for recursive nesting.
    :rtype: defaultdict[Any, Any]
    """

    return defaultdict(nested_dict)


def add_to_dict(
    structure: defaultdict[Any, Any],
    path: list[str],
    data: list[StandardReturn],
) -> defaultdict[Any, Any]:
    """
    Adds data to a nested dictionary structure based on a specified path.

    This function traverses a nested dictionary (`structure`) using a list of keys
    (`path`). If the path consists of a single key, the data is added directly to the
    corresponding level. Otherwise, the function recursively traverses deeper into the
    structure, creating nested dictionaries as needed, until the data is added at the
    specified location.

    Key concepts:
    - Deepcopy: The `deepcopy` function is used to ensure that the `data` is safely
      duplicated into the struc, avoiding unintended mutations of the original data.
    - Recursive Traversal: The function calls itself recursively to traverse and modify
      deeper levels of the nested dictionary.

    Example:
    ```python
    structure: defaultdict = nested_dict()
    path: list[str] = ['level1', 'level2', 'level3']
    data: list[StandardReturn] = [{'key': 'value'}]
    add_to_dict(structure, path, data)
    # defaultdict(defaultdict, {'level1': {'level2': {'level3': [{'key': 'value'}]}}})
    ```

    :param structure: The nested dictionary to modify.
    :type structure: defaultdict[Any, Any]
    :param path: A list of keys representing the path to the target location.
    :type path: list[str]
    :param data: The data to add at the specified path.
    :type data: list[StandardReturn]
    :return: The modified dictionary with the new data added.
    :rtype: defaultdict[Any, Any]
    """

    if len(path) == 1:
        structure[path[0]] = deepcopy(data)
    elif len(path) > 1:
        structure[path[0]] = add_to_dict(structure[path[0]], path[1:], data)

    return structure


def convert_to_regular_dict(d: dict[Any, Any]) -> dict[Any, Any]:
    """
    Converts a nested `defaultdict` into a regular dictionary.

    This function recursively traverses a `defaultdict` and its nested dictionaries,
    converting all instances of `defaultdict` into standard Python dictionaries. This
    ensures the resulting structure is free of `defaultdict` behavior.

    Key concepts:
    - defaultdict: A dictionary subclass from the `collections` module that provides
      default values for missing keys. This func removes that behavior by converting
      it into a regular dictionary.
    - Recursive Conversion: The function traverses and converts all nested dict,
      ensuring the entire structure is converted.

    Example:
    ```python
    d: defaultdict = nested_dict()
    d['level1']['level2'] = 'value'
    convert_to_regular_dict(d)
    # {'level1': {'level2': 'value'}}
    ```

    :param d: The dictionary to convert. Can include nested `defaultdict` instances.
    :type d: dict[Any, Any]
    :return: A dict where all `defaultdict` instances are converted to regular dicts.
    :rtype: dict[Any, Any]
    """

    if isinstance(d, defaultdict):
        d = {k: convert_to_regular_dict(v) for k, v in d.items()}

    return d


def standard_struct() -> StandardReturn:
    """
    Has the attribuition of returning an empty dict but maintaining the standard keys.

    The keys are listed below, followed by they types, as below:
    ```python
    dct: StandardReturn = {
        'statement': Statement,
        'name': str,
        'tokens': Tokens,
        'annot': str,
        'value': str,
        'decorators': Decorators,
        'inheritance': Inheritance,
        'path': str,
        'category': ImportType | FunctionType,
        'docstring': str | None,
        'rtype': str,
        'args': ArgsKwargs,
        'kwargs': ArgsKwargs,
        'test': str,
        'msg': str,
        'code': str,
    }
    ```
    Any other datatype different from those above must be avoided as much as possible
    to maintain the codebase at the same struct. Python is not the best when talking
    about types like Java or Rust, so keep this in mind is really necessary.

    Example:
    ```python
    standard_struct()
    # {}
    ```

    :return: An empty dict annotated with special custom type.
    :rtype: StandardReturn
    """

    data: StandardReturn = {}
    return data


def indent_code(code: str, level: int = 4) -> str:
    """
    Used just for applying indentation to code before building the doc `.md` file.

    By receiving the code itself and an indentation number, defaulting to 4, and for
    each line applies the desired indentation level, A.K.A leftpad.

    Example:
    ```python
    code: str = \"\"\"for i in range(10):\n\t\tstr(i)\"\"\"
    level: int = 4
    code
    # for i in range(10):\n#     str(i)
    indent_code(code, level)
    #     for i in range(10):\n#         str(i)
    ```

    :param code: The code snippet to be formatted.
    :type code: str
    :param level: The number of spaces to leftpad each line.
    :type level: int
    :return: The code snippet leftpadded.
    :rtype: str
    """

    indent = ' ' * level
    new_code = '\n'.join(
        map(lambda line: f'{indent}{line}' if line.strip() else '', code.splitlines())
    )

    return new_code
