from collections import defaultdict
from copy import deepcopy
from importlib.util import find_spec
from typing import Any

from custom_types import NodeHandler


def bin(item: Any, universe: list[Any] | tuple[Any]) -> bool:
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
    >>> lst: list[int] = [1,2,3,4,5]
    >>> num: int = 4
    >>> result: bool = bin(num, lst)
    True
    ```

    :param item: the item to check if exists in
    :type item: Any
    :param universe: the sorted iterable to be evaluated
    :type universe: list[Any] | tuple[Any]
    :return: if the item is found in the universe
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
    >>> result: bool = is_lib_installed('fastapi')
    False
    ```

    :param name: the name of the lib, e.g. numpy or numba
    :type name: str
    :return: whether the lib exists in the env
    :rtype: bool
    """

    try:
        spec = find_spec(name)
        return True if spec is not None else False
    except ModuleNotFoundError:
        return False


def nested_dict() -> dict[Any, Any]:
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
    >>> d = nested_dict()
    >>> d['level1']['level2']['level3'] = 'text'
    {'level': {'level2': {'level3': 'text'}}}
    ```

    :return: a `defaultdict` instance configured for recursive nesting
    :rtype: dict[Any, Any]
    """

    return defaultdict(nested_dict)


def add_to_dict(
    structure: dict[Any, Any],
    path: list[str],
    data: list[NodeHandler],
) -> dict[Any, Any]:
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
    >>> structure = {}
    >>> path = ['level1', 'level2', 'level3']
    >>> data = {'key': 'value'}
    >>> result = add_to_dict(structure, path, data)
    {'level1': {'level2': {'level3': {'key': 'value'}}}}
    ```

    :param structure: the nested dictionary to modify
    :type structure: dict[Any, Any]
    :param path: a list of keys representing the path to the target location
    :type path: list[str]
    :param data: the data to add at the specified path
    :type data: NodeHandler
    :return: the modified dictionary with the new data added
    :rtype: dict[Any, Any]
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
    >>> from collections import defaultdict


    >>> def nested_dict():
    ...     return defaultdict(nested_dict)


    >>> d = nested_dict()
    >>> d['level1']['level2'] = 'value'
    >>> regular_dict = convert_to_regular_dict(d)
    {'level1': {'level2': 'value'}}
    ```

    :param d: the dictionary to convert. Can include nested `defaultdict` instances
    :type d: dict[Any, Any]
    :return: a dict where all `defaultdict` instances are converted to regular dicts
    :rtype: dict[Any, Any]
    """

    if isinstance(d, defaultdict):
        d = {k: convert_to_regular_dict(v) for k, v in d.items()}

    return d
