from importlib.util import find_spec
from typing import Any


def bin(item: Any, universe: list[Any] | tuple[Any]) -> bool:
    """
    Binary Search algorithm which returns not the index, but a boolean.

    It inicializes two "pointers", one for the low or start of the iterator
    and another for the high or the end of it. Gets the middle point and
    compares it with the asked item.
    
    If the item is greater/after the middle the middle becomes the new low
    and repeats, otherwise, it becomes the new high and so on and so on and
    so on... until the item is found and returns True or not, returning False.

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
