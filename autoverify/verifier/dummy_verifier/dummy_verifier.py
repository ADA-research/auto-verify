from result import Err, Ok

from autoverify.verifier import CompleteVerifier
from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
)


class DummyVerifier(CompleteVerifier):
    def verify_property(self, property, network) -> CompleteVerificationResult:
        outcome = CompleteVerificationOutcome("SAT", None)
        return Ok(outcome)

    def sample_configuration(self, config_levels: set[int], size: int):
        return super().sample_configuration(config_levels, size)
