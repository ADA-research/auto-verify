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
        self,
        *,
        config_levels: set[ConfigurationLevel] = {ConfigurationLevel.VERIFIER},
        size: int = 1,
    ):
        """_summary_."""
        for config_level, config_space in self.config_spaces.items():
            print(config_space.sample_configuration())
