import string
import sys
from pathlib import Path


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
    if L < len(haystack) and haystack[L] not in string.whitespace:
        return False

    return True
