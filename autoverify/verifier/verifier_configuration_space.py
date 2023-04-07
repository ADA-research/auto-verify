"""Verifier configuration class to sample configurations from."""

from dataclasses import dataclass
from enum import Enum, auto

from ConfigSpace import ConfigurationSpace


class ConfigurationLevel(Enum):
    """Levels from which configurations can be sampled."""

    SOLVER = auto()
    """Embedded solver level, e.g. Gurobi parameters."""

    VERIFIER = auto()
    """Verification tool level"""


@dataclass
class VerifierConfigurationSpace:
    """_summary_."""

    config_spaces: dict[ConfigurationLevel, ConfigurationSpace]

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        raise NotImplementedError
