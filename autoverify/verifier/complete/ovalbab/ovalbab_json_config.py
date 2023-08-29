"""_summary_."""
import json
from pathlib import Path
from typing import IO, Any

from ConfigSpace import Configuration

from autoverify.util.dict import nested_set
from autoverify.util.tempfiles import tmp_json_file_from_dict


class OvalbabJsonConfig:
    """Class for Oval-BaB JSON configs."""

    def __init__(self, json_file: IO[str]):
        """_summary_."""
        self._json_file = json_file

    @classmethod
    def from_json(cls, json_file: Path):
        """_summary."""
        ovalbab_dict: dict[str, Any]

        with open(str(json_file)) as f:
            ovalbab_dict = json.load(f)

        return cls(tmp_json_file_from_dict(ovalbab_dict))

    @classmethod
    def from_config(cls, config: Configuration):
        """_summary."""
        dict_config: dict[str, Any] = dict(config)
        ovalbab_dict: dict[str, Any] = {
            "bounding": {
                "nets": [
                    {
                        "params": {"betas": [0.9, 0.999]},
                    },
                    {
                        "params": {
                            "betas": [0.9, 0.999],
                            "init_params": {"betas": [0.9, 0.999]},
                        }
                    },
                ]
            }
        }

        for key, value in dict_config.items():
            if value == "null":
                value = None  # cant directly use `None` in configspace

            nested_keys = key.split("__")
            sub_dict = ovalbab_dict

            if len(nested_keys) >= 2:
                if nested_keys[1].startswith("nets"):
                    i = int(nested_keys[1][-1]) - 1
                    sub_dict = sub_dict["bounding"]["nets"][i]
                    nested_keys = nested_keys[2:]

            if nested_keys[-1] == "best_among" and value:
                value = value.split("__")

            nested_set(sub_dict, nested_keys, value)

        return cls(tmp_json_file_from_dict(ovalbab_dict))

    def get_json_file(self) -> IO[str]:
        """_summary_."""
        return self._json_file

    def get_json_file_path(self) -> Path:
        """_summary_."""
        return Path(self._json_file.name)
