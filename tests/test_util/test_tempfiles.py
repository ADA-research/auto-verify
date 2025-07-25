import json
import os

import yaml
from autoverify.util.tempfiles import (
    tmp_file,
    tmp_json_file,
    tmp_json_file_from_dict,
    tmp_yaml_file,
    tmp_yaml_file_from_dict,
)


def test_tmp_file():
    temp_file = tmp_file(".txt")

    assert temp_file.name.endswith(".txt")
    assert os.path.exists(temp_file.name)


def test_tmp_json_file():
    temp_json_file = tmp_json_file()

    assert temp_json_file.name.endswith(".json")
    assert os.path.exists(temp_json_file.name)


def test_tmp_json_file_from_dict():
    test_dict = {"foo": "hello", "bar": 42}
    temp_json_file = tmp_json_file_from_dict(test_dict)

    assert temp_json_file.name.endswith(".json")
    assert os.path.exists(temp_json_file.name)

    with open(temp_json_file.name) as fp:
        data = json.load(fp)
        assert data == test_dict


def test_tmp_yaml_file():
    temp_yaml_file = tmp_yaml_file()

    assert temp_yaml_file.name.endswith(".yaml")
    assert os.path.exists(temp_yaml_file.name)


def test_tmp_yaml_file_from_dict():
    test_dict = {"foo": "hello", "bar": 42}
    temp_yaml_file = tmp_yaml_file_from_dict(test_dict)

    assert temp_yaml_file.name.endswith(".yaml")
    assert os.path.exists(temp_yaml_file.name)

    with open(temp_yaml_file.name) as fp:
        data = yaml.safe_load(fp)
        assert data == test_dict
