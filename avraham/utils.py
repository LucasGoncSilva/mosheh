from typing import Any


def binary_search(item: Any, universe: list | tuple) -> int:
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
            return mid

    return -1
