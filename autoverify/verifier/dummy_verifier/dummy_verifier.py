"""Temporary dummy verifier."""

from copy import deepcopy

from result import Ok

from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
)
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verifier.verifier_configuration_space import (
    VerifierConfigurationSpace,
)

from .dummy_configspace import DummyConfigspace


class DummyVerifier(CompleteVerifier):
    """_summary_."""

    _name: str = "DummyVerifier"
    _verifier_configuration_space: VerifierConfigurationSpace = deepcopy(
        DummyConfigspace
    )

    def verify_property(self, property, network) -> CompleteVerificationResult:
        """_summary_."""
        # temp silence warnings
        property, network = 0, 0
        property, network = network, property

        outcome = CompleteVerificationOutcome("SAT", None)
        return Ok(outcome)

    def sample_configuration(self, config_levels: set[int], size: int):
        """_summary_."""
        return super().sample_configuration(config_levels, size)
