"""TODO docstring."""
from abc import ABC, abstractmethod
from pathlib import Path

from autoverify.cli.install import TOOL_DIR_NAME, VERIFIER_DIR
from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)


class Verifier(ABC):
    """Abstract class to represent a verifier tool."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique verifier name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def verifier_configspace(self) -> VerifierConfigurationSpace:
        """Verifier configuration space to sample from."""
        raise NotImplementedError

    @property
    def tool_path(self) -> Path:
        """The path where the verifier is installed."""
        tool_path = VERIFIER_DIR / self.name / TOOL_DIR_NAME
        print(tool_path)

        if not tool_path.exists():
            raise FileNotFoundError(
                f"Could not find installation for tool {self.name}"
            )

        return Path(tool_path)  # mypy complains tool_path is any


class CompleteVerifier(Verifier):
    """_summary_."""

    @abstractmethod
    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        """_summary_.

        _detailed_

        Args:
            property (_type_): _description_
            network (_type_): _description_

        Returns:
            CompleteVerificationResult: _description_
        """
        raise NotImplementedError

    @abstractmethod  # TODO: return type
    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_.

        _detailed_

        Args:
            property (_type_): _description_
            network (_type_): _description_

        Returns:
            list[VerifierConfiguration]: _description_
        """
        raise NotImplementedError
