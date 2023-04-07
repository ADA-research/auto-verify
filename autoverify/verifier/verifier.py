"""TODO docstring."""

from abc import ABC, abstractmethod

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


class CompleteVerifier(Verifier):
    """_summary_."""

    @abstractmethod
    def verify_property(self, property, network) -> CompleteVerificationResult:
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
