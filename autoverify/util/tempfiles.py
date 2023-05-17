"""YAML file utils."""
import json
import tempfile
from typing import IO, Any

import yaml


def tmp_file(extension: str) -> IO[str]:
    """Return a new tempfile with the given extension"""
    return tempfile.NamedTemporaryFile("w", suffix=extension)


# TODO: Just make a functin that returns a tempfile with extension as param
def tmp_json_file() -> IO[str]:
    """Returns a new temporary named empty yaml file."""
    return tempfile.NamedTemporaryFile("w", suffix=".json")


def tmp_json_file_from_dict(a_dict: dict[Any, Any]) -> IO[str]:
    """Returns a new temporary named json file with the dict written to it."""
    tmp_json = tmp_json_file()

    with open(tmp_json.name, "w") as fp:
        json.dump(a_dict, fp)

    return tmp_json


def tmp_yaml_file() -> IO[str]:
    """Returns a new temporary named empty yaml file."""
    return tempfile.NamedTemporaryFile("w", suffix=".yaml")


def tmp_yaml_file_from_dict(a_dict: dict[Any, Any]) -> IO[str]:
    """Returns a new temporary named yaml file with the dict written to it."""
    tmp_yaml = tmp_yaml_file()
    yaml.dump(a_dict, tmp_yaml)

    return tmp_yaml
