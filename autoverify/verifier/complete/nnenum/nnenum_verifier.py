"""Nnenum verifier."""
# TODO: More links and details in above docstring
from pathlib import Path

from result import Ok

from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
)
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)

from .nnenum_configspace import DummyConfigspace


class Nnenum(CompleteVerifier):
    """_summary_."""

    name: str = "nnenum"
    verifier_configspace: VerifierConfigurationSpace = DummyConfigspace

    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        print(self.tool_path)
        result = CompleteVerificationOutcome("UNSAT", None)
        return Ok(result)

    # TODO:
    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return super().sample_configuration(config_levels, size)
