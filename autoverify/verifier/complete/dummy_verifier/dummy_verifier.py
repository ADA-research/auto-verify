"""Temporary dummy verifier."""
from ConfigSpace import ConfigurationSpace
from result import Ok

from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
)
from autoverify.verifier.verifier import CompleteVerifier

from .dummy_configspace import DummyConfigspace


class DummyVerifier(CompleteVerifier):
    """_summary_."""

    name: str = "DummyVerifier"
    config_space: ConfigurationSpace = DummyConfigspace

    def verify_property(self, network, property) -> CompleteVerificationResult:
        """_summary_."""
        # temp silence warnings
        property, network = 0, 0
        property, network = network, property

        outcome = CompleteVerificationOutcome("SAT", None)
        return Ok(outcome)
