"""CLI utility."""

import ast
from argparse import ArgumentTypeError
from typing import Any

from ConfigSpace import Configuration, ConfigurationSpace


def parse_config_str_type(value: str, cfg_space: ConfigurationSpace) -> Configuration:
    """Type to use in `argparse` for a verifier configuration."""
    cfg_dict: dict[str, Any] = {}

    try:
        cfg_dict = ast.literal_eval(value)
        return Configuration(cfg_space, values=cfg_dict)
    except Exception as err:
        raise ArgumentTypeError("Failed to create configuration from arg.") from err
