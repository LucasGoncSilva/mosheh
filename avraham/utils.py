from importlib.util import find_spec
from typing import Any


def bin(item: Any, universe: list[Any] | tuple[Any]) -> bool:
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
    try:
        spec = find_spec(name)
        return True if spec is not None else False
    except ModuleNotFoundError:
        return False
