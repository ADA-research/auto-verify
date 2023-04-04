"""TODO docstring."""

from abc import ABC, abstractmethod

from attrs import define, field

from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier_configuration_space import (
    VerifierConfigurationSpace,
)


@define
class Verifier(ABC):
    """Abstract class to represent a verifier tool."""

    _name: str = field(init=False)
    _verifier_configuration_space: VerifierConfigurationSpace = field(
        init=False
    )


@define
class CompleteVerifier(Verifier):
    """Abstract class to represent complete verification tool."""

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
