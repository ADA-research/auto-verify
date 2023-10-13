from autoverify.util.dict import nested_del, nested_get, nested_set


def test_nested_get():
    data = {"a": {"b": {"c": 42}}}
    keys = ["a", "b", "c"]
    result = nested_get(data, keys)
    assert result == 42


def test_nested_set():
    data = {}
    keys = ["a", "b", "c"]
    value = 42
    nested_set(data, keys, value)
    assert data == {"a": {"b": {"c": 42}}}


def test_nested_del():
    data = {"a": {"b": {"c": 42}}}
    keys = ["a", "b", "c"]
    nested_del(data, keys)
    assert data == {"a": {"b": {}}}
