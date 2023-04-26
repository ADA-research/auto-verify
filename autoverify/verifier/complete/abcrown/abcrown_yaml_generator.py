import tempfile
from pathlib import Path
from typing import IO

import yaml


def tmp_yaml_file() -> IO[str]:
    return tempfile.NamedTemporaryFile("w", suffix=".yaml")


def simple_abcrown_config(property: Path, network: Path) -> IO[str]:
    simple_config = {
        "model": {"onnx_path": str(network)},
        "specification": {"vnnlib_path": str(property)},
        "solver": {"batch_size": 2048},
    }

    tmp_yaml = tmp_yaml_file()
    yaml.dump(simple_config, tmp_yaml)

    return tmp_yaml
