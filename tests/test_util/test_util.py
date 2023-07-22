import pytest

from autoverify.util import (
    find_substring,
    get_python_path,
    is_list_of_strings,
    is_serializable,
)


def test_find_substring():
    haystack = "foo\nbar\nbarr\nsafeX"

    assert find_substring("bar", haystack)
    assert find_substring("barr", haystack)

    # Whole words only
    assert not find_substring("safe", haystack)
    assert find_substring("safeX", haystack)


def test_get_python_path():
    py_path = get_python_path()

    # TODO: Check if its actually python
    assert py_path.is_file()


def test_is_list_of_strings():
    assert not is_list_of_strings([])
    assert is_list_of_strings(["hello", "world"])
    assert not is_list_of_strings([1, 2, 3])
    assert not is_list_of_strings(["hello", 1, "world"])


@pytest.mark.parametrize(
    "var, expected",
    [
        ("hello world", True),
        ([1, 2, 3], True),
        (4.567, True),
        (True, True),
        (None, True),
        (object(), False),
        ({"key": "value"}, True),
    ],
)
def test_is_serializable(var, expected):
    assert is_serializable(var) == expected
