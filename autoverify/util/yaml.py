"""YAML file utils."""
import tempfile
from typing import IO, Any

import yaml


def tmp_yaml_file() -> IO[str]:
    """Returns a new temporary named empty yaml file."""
    return tempfile.NamedTemporaryFile("w", suffix=".yaml")


def tmp_yaml_file_from_dict(a_dict: dict[Any, Any]) -> IO[str]:
    """Returns a new temporary named yaml file with the dict written to it."""
    tmp_yaml = tmp_yaml_file()
    yaml.dump(a_dict, tmp_yaml)

    return tmp_yaml
