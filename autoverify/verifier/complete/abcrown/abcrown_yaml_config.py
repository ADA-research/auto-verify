"""File for generating abcrown configs."""

from pathlib import Path
from typing import IO, Any

import yaml
from ConfigSpace import Configuration

from autoverify.util.dict import nested_set
from autoverify.util.tempfiles import tmp_yaml_file, tmp_yaml_file_from_dict


class AbcrownYamlConfig:
    """Class for ab-crown YAML configs."""

    def __init__(self, yaml_file: IO[str] | str | Path):
        """New instance.
        
        Args:
            yaml_file: Either a file object, file path string, or Path object
        """
        self._yaml_file = yaml_file

    @classmethod
    def from_yaml(
        cls,
        yaml_file: Path,
        network: Path,
        property: Path,
        *,
        batch_size: int = 64,
        yaml_override: dict[str, Any] | None = None,
    ):
        """Create new instance from a YAML file."""
        abcrown_dict = yaml.safe_load(yaml_file.read_text())

        nested_set(abcrown_dict, ["model", "onnx_path"], str(network))
        nested_set(
            abcrown_dict, ["specification", "vnnlib_path"], str(property)
        )
        nested_set(abcrown_dict, ["general", "save_adv_example"], True)
        nested_set(abcrown_dict, ["solver", "batch_size"], batch_size)

        if yaml_override:
            for k, v in yaml_override.items():
                nested_set(abcrown_dict, k.split("__"), v)

        with tmp_yaml_file() as new_yaml_file:
            yaml.dump(abcrown_dict, new_yaml_file)
            return cls(new_yaml_file)

    @classmethod
    def from_config(
        cls,
        config: Configuration,
        network: Path,
        property: Path,
        *,
        batch_size: int = 512,
        yaml_override: dict[str, Any] | None = None,
    ):
        """Initialize the YAML file based on the configuration."""
        dict_config: dict[str, Any] = dict(config)
        abcrown_dict: dict[str, Any] = {}

        for key, value in dict_config.items():
            nested_keys = key.split("__")
            nested_set(abcrown_dict, nested_keys, value)

        nested_set(abcrown_dict, ["model", "onnx_path"], str(network))
        nested_set(
            abcrown_dict, ["specification", "vnnlib_path"], str(property)
        )
        nested_set(abcrown_dict, ["general", "save_adv_example"], True)
        nested_set(abcrown_dict, ["solver", "batch_size"], batch_size)

        if yaml_override:
            for k, v in yaml_override.items():
                nested_set(abcrown_dict, k.split("__"), v)

        return cls(tmp_yaml_file_from_dict(abcrown_dict))

    def get_yaml_file(self) -> IO[str]:
        """Get the ab-crown YAML config file."""
        if isinstance(self._yaml_file, str | Path):
            return open(str(self._yaml_file))
        if not self._yaml_file:
            raise FileNotFoundError("YAML file was not made yet.")
        return self._yaml_file

    def get_yaml_file_path(self) -> Path:
        """Get the path to the ab-crown YAML config file."""
        if isinstance(self._yaml_file, str | Path):
            return Path(str(self._yaml_file))
        return Path(self._yaml_file.name)
