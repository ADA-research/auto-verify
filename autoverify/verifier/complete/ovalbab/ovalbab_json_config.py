"""Intermediate representation of ovalbab json configs."""

import json
from pathlib import Path
from typing import IO, Any

from ConfigSpace import Configuration

from autoverify.util.dict import nested_set
from autoverify.util.tempfiles import tmp_json_file_from_dict


class OvalbabJsonConfig:
    """Class for Oval-BaB JSON configs."""

    def __init__(self, json_file: IO[str] | str | Path):
        """New instance.

        Args:
            json_file: Either a file object, file path string, or Path object
        """
        self._json_file = json_file

    @classmethod
    def from_json(cls, json_file: Path):
        """New instance from a JSON file."""
        ovalbab_dict: dict[str, Any]

        with open(str(json_file)) as f:
            ovalbab_dict = json.load(f)

        return cls(tmp_json_file_from_dict(ovalbab_dict))

    @classmethod
    def from_config(cls, config: Configuration):
        """New instance from a Configuration."""
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

            if len(nested_keys) >= 2 and nested_keys[1].startswith("nets"):
                i = int(nested_keys[1][-1]) - 1
                sub_dict = sub_dict["bounding"]["nets"][i]
                nested_keys = nested_keys[2:]

            if nested_keys[-1] == "best_among" and value:
                value = value.split("__")

            nested_set(sub_dict, nested_keys, value)

        return cls(tmp_json_file_from_dict(ovalbab_dict))

    def get_json_file(self) -> IO[str]:
        """Return the json file."""
        if isinstance(self._json_file, str | Path):
            return open(str(self._json_file))
        return self._json_file

    def get_json_file_path(self) -> Path:
        """The path to the json file."""
        if isinstance(self._json_file, str | Path):
            return Path(str(self._json_file))
        return Path(self._json_file.name)
