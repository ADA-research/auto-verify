"""_summary_."""
import ast
import re
from typing import Any

from ConfigSpace import Configuration, ConfigurationSpace


def config_dict_from_config_str(cfg: str) -> dict[str, Any]:
    """_summary_."""
    cfg = re.sub(r"^.*?{", "{", cfg)
    return ast.literal_eval(cfg[:-1])


def config_from_str(cfg: str, cfg_space: ConfigurationSpace) -> Configuration:
    """_summary_."""
    return Configuration(cfg_space, config_dict_from_config_str(cfg))
