"""File for generating abcrown configs."""
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify.util.dict import nested_set
from autoverify.util.yaml import tmp_yaml_file_from_dict


@dataclass
class AbcrownYamlConfig:
    """Class for ab-crown YAML configs."""

    property: Path
    network: Path
    configuration: Configuration = ConfigurationSpace().sample_configuration()

    def __post_init__(self):
        """Initialize the YAML file based on the configuration."""
        dict_config: dict[str, Any] = self.configuration.get_dictionary()
        abcrown_dict: dict[str, Any] = {}

        for key, value in dict_config.items():
            nested_keys = key.split("__")
            nested_set(abcrown_dict, nested_keys, value)

        nested_set(abcrown_dict, ["model", "onnx_path"], str(self.network))
        nested_set(
            abcrown_dict, ["specification", "vnnlib_path"], str(self.property)
        )

        self._yaml_file: IO[str] = tmp_yaml_file_from_dict(abcrown_dict)

    def get_yaml_file(self) -> IO[str]:
        """Get the ab-crown YAML config file."""
        if not self._yaml_file:
            raise FileNotFoundError("YAML file was not made yet.")

        return self._yaml_file
