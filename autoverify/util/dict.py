"""Dictionary utilities."""

from typing import Any


# credits @DomTomCat for nested functions
def nested_get(dic: dict[Any, Any], keys: list[str]):
    """Get a nested dict value from a list of string keys."""
    for key in keys:
        dic = dic[key]

    return dic


def nested_set(dic: dict[Any, Any], keys: list[str], value: Any):
    """Set a nested dict value from a list of string keys."""
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})

    dic[keys[-1]] = value


def nested_del(dic: dict[Any, Any], keys: list[str]):
    """Det a nested dict value from a list of string keys."""
    for key in keys[:-1]:
        dic = dic[key]

    del dic[keys[-1]]
