"""_summary_."""

import ast
import re
from pathlib import Path
from typing import Any

from ConfigSpace import Configuration, ConfigurationSpace


def config_dict_from_config_str(cfg: str) -> dict[str, Any]:
    """Create a config object from a printed configuration."""
    cfg = re.sub(r"^.*?{", "{", cfg)
    dic: dict[str, Any] = ast.literal_eval(cfg[:-1])
    return dic


def config_from_str(cfg: str, cfg_space: ConfigurationSpace) -> Configuration:
    """Create a config object from a string configuration."""
    return Configuration(cfg_space, config_dict_from_config_str(cfg))


def config_from_txt_file(
    file: Path, cfg_space: ConfigurationSpace
) -> Configuration:
    """Create a config from a config in a txt file."""
    with open(str(file), "r") as f:
        txt = f.read().rstrip()

    return config_from_str(txt, cfg_space)


def config_from_file(
    file: Path, cfg_space: ConfigurationSpace
) -> Configuration:
    """Create a config from a config in a file."""
    if file.suffix == ".txt":
        return config_from_txt_file(file, cfg_space)
    else:
        raise ValueError(f"File type {file.suffix} not supported, use txt.")
