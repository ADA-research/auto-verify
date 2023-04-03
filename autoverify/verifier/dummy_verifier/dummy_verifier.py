"""Temporary dummy verifier."""

from result import Ok

from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
)
from autoverify.verifier.verifier import CompleteVerifier


class DummyVerifier(CompleteVerifier):
    """_summary_."""

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
