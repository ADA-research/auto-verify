import json
import string
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any, TypeVar

basestring = (str, bytes)


def get_python_path() -> Path:
    """Returns the path to the current Python executable."""
    return Path(sys.executable)


# credits: @aaronasterling
def find_substring(needle: str, haystack: str) -> bool:
    """Finds a whole word in a substring.

    Args:
        needle: The word to find.
        haystack: The text to find the word in.

    Returns:
        bool: True if the whole word was found, false otherwise.
    """
    index = haystack.find(needle)

    if index == -1:
        return False

    if index != 0 and haystack[index - 1] not in string.whitespace:
        return False

    L = index + len(needle)
    return not (len(haystack) > L and haystack[L] not in string.whitespace)


def is_list_of_strings(lst: list[Any]) -> bool:
    """Check if a list contains strings only."""
    if lst and isinstance(lst, list):
        return all(isinstance(elem, basestring) for elem in lst)
    else:
        return False


def is_serializable(var: Any) -> bool:
    """Check if a variable or object is serializable."""
    try:
        json.dumps(var)
        return True
    except (TypeError, OverflowError):
        return False


def add_to_average(average: float, value: float, size: int) -> float:
    """Update an average with a new value."""
    return (size * average + value) / (size + 1)


_T = TypeVar("_T")


def merge_lists(*lists: list[_T]) -> list[_T]:
    """Merge multiple lists."""
    uniq = set()

    for lst in lists:
        uniq.update(set(lst))

    return list(uniq)


def set_iter_except(s: set[_T], e: _T) -> Iterator[_T]:
    """Iterate the set, ignoring one element."""
    for item in s:
        if item != e:
            yield item
