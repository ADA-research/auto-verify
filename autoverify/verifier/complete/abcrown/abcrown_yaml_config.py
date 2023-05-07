"""File for generating abcrown configs."""
from pathlib import Path
from typing import IO, Any

import yaml
from ConfigSpace import Configuration

from autoverify.util.dict import nested_set
from autoverify.util.yaml import tmp_yaml_file, tmp_yaml_file_from_dict


class AbcrownYamlConfig:
    """Class for ab-crown YAML configs."""

    def __init__(self, yaml_file: IO[str]):
        """_summary_."""
        self._yaml_file = yaml_file

    @classmethod
    def from_yaml(
        cls,
        yaml_file: Path,
        network: Path,
        property: Path,
    ):
        """_summary_."""
        abcrown_dict = yaml.safe_load(str(yaml_file))

        nested_set(abcrown_dict, ["model", "onnx_path"], str(network))
        nested_set(
            abcrown_dict, ["specification", "vnnlib_path"], str(property)
        )
        nested_set(abcrown_dict, ["general", "save_adv_example"], True)

        new_yaml_file = tmp_yaml_file()
        yaml.dump(abcrown_dict, new_yaml_file)

        return cls(new_yaml_file)

    @classmethod
    def from_config(
        cls,
        network: Path,
        property: Path,
        configuration: Configuration,
    ):
        """Initialize the YAML file based on the configuration."""
        dict_config: dict[str, Any] = configuration.get_dictionary()
        abcrown_dict: dict[str, Any] = {}

        for key, value in dict_config.items():
            nested_keys = key.split("__")
            nested_set(abcrown_dict, nested_keys, value)

        nested_set(abcrown_dict, ["model", "onnx_path"], str(network))
        nested_set(
            abcrown_dict, ["specification", "vnnlib_path"], str(property)
        )
        nested_set(abcrown_dict, ["general", "save_adv_example"], True)

        return cls(tmp_yaml_file_from_dict(abcrown_dict))

    def get_yaml_file(self) -> IO[str]:
        """Get the ab-crown YAML config file."""
        if not self._yaml_file:
            raise FileNotFoundError("YAML file was not made yet.")

        return self._yaml_file
