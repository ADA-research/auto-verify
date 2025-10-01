"""Configuration system for auto-verify.

This module provides configuration options for choosing between
different environment management strategies (conda vs venv) and other
user preferences.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

try:
    import tomllib
except ImportError:
    import tomli as tomllib
from xdg_base_dirs import xdg_config_home, xdg_data_home

EnvStrategy = Literal["conda", "venv", "auto"]


@dataclass
class AutoVerifyConfig:
    """Configuration for auto-verify installation and runtime."""

    # Environment management strategy
    env_strategy: EnvStrategy = "conda"  # Default to conda as recommended

    # Installation paths
    custom_install_path: Path | None = None

    # Runtime preferences
    prefer_gpu: bool = True
    default_timeout: int = 600

    # Logging
    log_level: str = "INFO"
    verbose_installation: bool = False

    # Advanced options
    allow_conda_fallback: bool = True
    require_uv: bool = False

    @classmethod
    def default(cls) -> "AutoVerifyConfig":
        """Create default configuration."""
        return cls()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AutoVerifyConfig":
        """Create configuration from dictionary."""
        config = cls()

        for key, value in data.items():
            if hasattr(config, key):
                # Handle Path conversion
                if key.endswith("_path") and value is not None:
                    value = Path(value)
                setattr(config, key, value)

        return config

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Path):
                result[key] = str(value)
            elif value is None:
                # Handle None values - tomli-w can't serialize None
                if key == "custom_install_path":
                    # Skip None paths
                    continue
                else:
                    # For other None values, use appropriate defaults
                    if key == "env_strategy":
                        result[key] = "auto"
                    elif isinstance(getattr(self.__class__, key, None), property):
                        # Skip properties
                        continue
                    elif key.startswith("_"):
                        # Skip private attributes
                        continue
                    else:
                        # Use empty string for other None values
                        result[key] = ""
            else:
                result[key] = value
        return result


class ConfigManager:
    """Manages auto-verify configuration."""

    CONFIG_FILE_NAME = "autoverify.toml"

    def __init__(self):
        self.config_dir = xdg_config_home() / "autoverify"
        self.config_file = self.config_dir / self.CONFIG_FILE_NAME
        self._config: AutoVerifyConfig | None = None

    def get_config(self) -> AutoVerifyConfig:
        """Get the current configuration, loading from file if necessary."""
        if self._config is None:
            self._config = self.load_config()
        return self._config

    def load_config(self) -> AutoVerifyConfig:
        """Load configuration from file."""
        if not self.config_file.exists():
            return AutoVerifyConfig.default()

        try:
            with open(self.config_file, "rb") as f:
                data = tomllib.load(f)
            return AutoVerifyConfig.from_dict(data)
        except Exception as e:
            print(f"Warning: Failed to load config from {self.config_file}: {e}")
            return AutoVerifyConfig.default()

    def save_config(self, config: AutoVerifyConfig):
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        try:
            import tomli_w
        except ImportError:
            print("Warning: tomli-w not available, cannot save config. Install with: pip install tomli-w")
            return

        try:
            with open(self.config_file, "wb") as f:
                tomli_w.dump(config.to_dict(), f)
            self._config = config
        except Exception as e:
            print(f"Warning: Failed to save config to {self.config_file}: {e}")

    def set_env_strategy(self, strategy: EnvStrategy):
        """Set the environment strategy and save."""
        config = self.get_config()
        config.env_strategy = strategy
        self.save_config(config)
        print(f"Environment strategy set to: {strategy}")

    def reset_config(self):
        """Reset configuration to defaults."""
        config = AutoVerifyConfig.default()
        self.save_config(config)
        print("Configuration reset to defaults")


# Global config manager instance
_config_manager = ConfigManager()


def get_config() -> AutoVerifyConfig:
    """Get the global auto-verify configuration."""
    return _config_manager.get_config()


def set_env_strategy(strategy: EnvStrategy):
    """Set the environment management strategy."""
    _config_manager.set_env_strategy(strategy)


def get_env_strategy() -> EnvStrategy:
    """Get the current environment management strategy."""
    return get_config().env_strategy


def should_use_venv() -> bool:
    """Determine if venv should be used based on configuration and
    availability."""
    config = get_config()
    strategy = config.env_strategy

    if strategy == "venv":
        return True
    elif strategy == "conda":
        return False
    elif strategy == "auto":
        # Auto-detect: prefer venv if uv is available, otherwise use conda
        try:
            import subprocess

            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fall back to conda if available
            if config.allow_conda_fallback:
                try:
                    from autoverify.util.conda import is_conda_installed

                    return not is_conda_installed()
                except ImportError:
                    pass
            return False

    return False


def get_install_path() -> Path:
    """Get the installation path for verifiers based on configuration.

    Returns:
        Path: The installation path to use
    """
    config = get_config()
    if config.custom_install_path:
        return config.custom_install_path

    # Default paths based on environment strategy
    if should_use_venv():
        return xdg_data_home() / "autoverify-venv"
    else:
        return xdg_data_home() / "autoverify"


def create_example_config():
    """Create an example configuration file for users."""
    config_dir = xdg_config_home() / "autoverify"
    example_file = config_dir / "autoverify.example.toml"

    config_dir.mkdir(parents=True, exist_ok=True)

    example_content = """# Auto-verify Configuration
# Choose environment management strategy: "conda" (recommended), "venv", or "auto"
env_strategy = "conda"

# Custom installation path (optional)
# custom_install_path = "/path/to/custom/location"

# Runtime preferences
prefer_gpu = true
default_timeout = 600

# Logging
log_level = "INFO"
verbose_installation = false

# Advanced options
allow_conda_fallback = true
require_uv = false
"""

    with open(example_file, "w") as f:
        f.write(example_content)

    print(f"Example configuration created at: {example_file}")
    print(f"Copy to: {config_dir / 'autoverify.toml'} and modify as needed")
    print("\nNote: conda is the recommended environment management strategy for auto-verify")


if __name__ == "__main__":
    create_example_config()
