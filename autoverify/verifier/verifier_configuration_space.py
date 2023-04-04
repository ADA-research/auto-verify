"""Verifier configuration class to sample configurations from."""

from enum import Enum, auto

from attrs import define, field
from ConfigSpace import ConfigurationSpace


class ConfigurationLevel(Enum):
    """Levels from which configurations can be sampled."""

    SOLVER = auto()
    """Embedded solver level, e.g. Gurobi parameters."""

    VERIFIER = auto()
    """Verification tool level"""


@define
class VerifierConfigurationSpace:
    """_summary_."""

    _configuration_spaces: dict[ConfigurationLevel, ConfigurationSpace] = field(
        init=True
    )

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        pass
