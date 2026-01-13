"""File for generating SDP-CROWN configs."""

from pathlib import Path
from typing import IO, Any

import yaml
from ConfigSpace import Configuration

from autoverify.util.tempfiles import tmp_yaml_file, tmp_yaml_file_from_dict


class SDPCrownYamlConfig:
    """Class for SDP-CROWN YAML configs."""

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
        *,
        yaml_override: dict[str, Any] | None = None,
    ):
        """Create new instance from a YAML file.

        Args:
            yaml_file: Path to YAML config file
            yaml_override: Optional dict to override YAML values

        Returns:
            SDPCrownYamlConfig instance
        """
        sdpcrown_dict = yaml.safe_load(yaml_file.read_text())

        if yaml_override:
            raise NotImplementedError("from_yaml: YAML override not supported for SDP-CROWN")

        with tmp_yaml_file() as new_yaml_file:
            yaml.dump(sdpcrown_dict, new_yaml_file)
            return cls(new_yaml_file)

    @classmethod
    def from_config(
        cls,
        config: Configuration,
        *,
        yaml_override: dict[str, Any] | None = None,
    ):
        """Initialize the YAML file based on the configuration.

        Args:
            config: ConfigSpace Configuration object
            yaml_override: Optional dict to override config values

        Returns:
            SDPCrownYamlConfig instance
        """
        sdpcrown_dict: dict[str, Any] = dict(config)

        if yaml_override:
            raise NotImplementedError("from_config: YAML override not supported for SDP-CROWN")

        return cls(tmp_yaml_file_from_dict(sdpcrown_dict))

    def get_config_dict(self) -> dict[str, Any]:
        """Get the SDP-CROWN config as a dictionary.

        Returns:
            Configuration dictionary
        """
        if isinstance(self._yaml_file, (str, Path)):
            with open(str(self._yaml_file)) as f:
                return yaml.safe_load(f)
        if not self._yaml_file:
            raise FileNotFoundError("YAML file was not made yet.")
        # If file object, read from current position
        self._yaml_file.seek(0)
        return yaml.safe_load(self._yaml_file)

    def get_yaml_file(self) -> IO[str]:
        """Get the SDP-CROWN YAML config file."""
        if isinstance(self._yaml_file, (str, Path)):
            return open(str(self._yaml_file))
        if not self._yaml_file:
            raise FileNotFoundError("YAML file was not made yet.")
        return self._yaml_file

    def get_yaml_file_path(self) -> Path:
        """Get the path to the SDP-CROWN YAML config file."""
        if isinstance(self._yaml_file, (str, Path)):
            return Path(str(self._yaml_file))
        return Path(self._yaml_file.name)

    def get_param(self, param: str, default: Any = None) -> Any:
        """Get a specific parameter from the config.

        Args:
            param: Parameter name to retrieve
            default: Default value if parameter not found

        Returns:
            Parameter value or default if not found
        """
        config = self.get_config_dict()
        return config.get(param, default)
