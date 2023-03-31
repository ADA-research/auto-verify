"""TODO docstring."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from autoverify.verifiers.types import CompleteVerificationResult


@dataclass
class Verifier(ABC):
    """Abstract class to represent a verifier tool.

    _detailed_

    Args:
        name:
            The unique name of the verifier.
        kind:
            Defines if the verifier is of the complete or incomplete kind.
        config_levels:
            Defines the available configuration levels that can be
            sampled from for this verifier.
    """

    name: str
    config_levels: set[int]


@dataclass
class CompleteVerifier(Verifier):
    """Abstract class to represent complete verification tools."""

    @abstractmethod  # TODO: param types
    def verify_property(self, property, network) -> CompleteVerificationResult:
        """_summary_.

        _detailed_

        Args:
            property (_type_): _description_
            network (_type_): _description_

        Returns:
            CompleteVerificationResult: _description_
        """
        pass

    @abstractmethod  # TODO: return type
    def sample_configuration(self, config_levels: set[int], size: int):
        """_summary_.

        _detailed_

        Args:
            property (_type_): _description_
            network (_type_): _description_

        Returns:
            list[VerifierConfiguration]: _description_
        """
        pass
