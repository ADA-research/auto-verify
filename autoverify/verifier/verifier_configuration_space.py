"""Verifier configuration class to sample configurations from."""

from dataclasses import dataclass
from enum import Enum

from ConfigSpace import Configuration, ConfigurationSpace


class ConfigurationLevel(Enum):
    """Levels from which configurations can be sampled."""

    VERIFIER = 1
    """Verification tool level"""

    SOLVER = 2
    """Embedded solver level, e.g. Gurobi parameters."""


# TODO: Support for sampling multiple levels at once
@dataclass
class VerifierConfigurationSpace:
    """_summary_."""

    config_spaces: dict[ConfigurationLevel, ConfigurationSpace]

    def sample_configuration(
        self,
        level: ConfigurationLevel,
        size: int = 1,
    ) -> Configuration:
        """_summary_."""
        if level not in self.config_spaces:
            raise Exception  # TODO: Proper exception type

        return self.config_spaces[level].sample_configuration(size=size)
