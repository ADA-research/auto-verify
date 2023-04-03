"""_summary_."""

from dataclasses import dataclass
from enum import IntEnum, auto

from ConfigSpace import ConfigurationSpace


class ConfigurationLevel(IntEnum):
    """Levels from which configurations can be sampled."""

    SOLVER = auto()
    """Embedded solver level, e.g. Gurobi parameters."""

    VERIFIER = auto()
    """Verification tool level"""


@dataclass
class VerifierConfiguration:
    """_summary_."""

    configuration_spaces: dict[ConfigurationLevel, ConfigurationSpace]

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        pass
