"""_summary_."""

from dataclasses import dataclass
from enum import IntEnum, auto

from ConfigSpace import ConfigurationSpace


class VerifierConfigurationLevel(IntEnum):
    """_summary_."""

    SOLVER = auto()
    VERIFIER = auto()


@dataclass
class VerifierConfiguration:
    """_summary_."""

    configuration_spaces: dict[VerifierConfigurationLevel, ConfigurationSpace]

    def sample_configuration(
        self, config_levels: set[VerifierConfigurationLevel], size: int
    ):
        """_summary_."""
        pass
