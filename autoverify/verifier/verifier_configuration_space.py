"""Verifier configuration class to sample configurations from."""

# from dataclasses import dataclass
from enum import Enum, auto

from ConfigSpace import ConfigurationSpace


class ConfigurationLevel(Enum):
    """Levels from which configurations can be sampled."""

    SOLVER = auto()
    """Embedded solver level, e.g. Gurobi parameters."""

    VERIFIER = auto()
    """Verification tool level"""


class VerifierConfigurationSpace:
    """_summary_."""

    def __init__(
        self, config_spaces: dict[ConfigurationLevel, ConfigurationSpace]
    ):
        """_summary_."""
        self._config_spaces = config_spaces

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        pass
