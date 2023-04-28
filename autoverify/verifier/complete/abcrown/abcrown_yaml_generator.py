"""File for generating abcrown configs."""
import tempfile
from pathlib import Path
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


def simple_abcrown_config(property: Path, network: Path) -> IO[str]:
    """Generate the simplest abcrown config for 1 onnx and 1 vnnlib."""
    simple_config = {
        "model": {"onnx_path": str(network)},
        "specification": {"vnnlib_path": str(property)},
        "solver": {"batch_size": 2048},
        "general": {"save_adv_example": True},
    }

    return tmp_yaml_file_from_dict(simple_config)
