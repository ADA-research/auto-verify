"""_summary_."""
import ast
import copy
import re
from pathlib import Path
from typing import Any, Final

from ConfigSpace import (
    Categorical,
    Configuration,
    ConfigurationSpace,
    EqualsCondition,
)


def config_dict_from_config_str(cfg: str) -> dict[str, Any]:
    """_summary_."""
    cfg = re.sub(r"^.*?{", "{", cfg)
    return ast.literal_eval(cfg[:-1])


def config_from_str(cfg: str, cfg_space: ConfigurationSpace) -> Configuration:
    """_summary_."""
    return Configuration(cfg_space, config_dict_from_config_str(cfg))


def config_from_txt_file(
    file: Path, cfg_space: ConfigurationSpace
) -> Configuration:
    """_summary_."""
    with open(str(file), "r") as f:
        txt = f.read().rstrip()

    return config_from_str(txt, cfg_space)


# def combine_configspaces(
#     *config_spaces: ConfigurationSpace,
# ) -> ConfigurationSpace:
#     """_summary_"""
#     if len(config_spaces) < 2:
#         raise ValueError("Provide at least 2 ConfigurationSpaces")
#
#     COMBINED_HP_NAME: Final[str] = "COMBINED_CFG_SPACE"
#     combined = ConfigurationSpace(name="combined")
#     names: dict[str, ConfigurationSpace] = {}
#
#     for i, v in enumerate(config_spaces):
#         if v.name in names:
#             raise ValueError("ConfigSpace names must be unique.")
#
#         if v.name == COMBINED_HP_NAME:
#             raise ValueError(f"Forbidden ConfigSpace name: {COMBINED_HP_NAME}")
#
#         if v.name is None:
#             v.name = str(i)
#
#         names[v.name or str(i)] = v
#
#     combined.add_hyperparameter(Categorical(COMBINED_HP_NAME, [*names.keys()]))
#
#     for name, space in names.items():
#         for hp in list(space.values()):
#             hp_copy = copy.deepcopy(hp)
#             combined.add_hyperparameter(hp_copy)
#             combined.add_condition(
#                 EqualsCondition(
#                     combined[hp_copy.name],
#                     combined[COMBINED_HP_NAME],
#                     name,
#                 )
#             )
#
#     return combined
