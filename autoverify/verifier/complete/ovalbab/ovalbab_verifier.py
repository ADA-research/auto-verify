"""Temporary ovalbab verifier."""
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

from .ovalbab_configspace import OvalBabConfigspace


class OvalBab(CompleteVerifier):
    """_summary_."""

    name: str = "ovalbab"
    verifier_configspace: VerifierConfigurationSpace = OvalBabConfigspace

    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        """_summary_."""
        # temp silence warnings
        property, network = network, property

        outcome = CompleteVerificationOutcome("SAT", None)
        return Ok(outcome)

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return super().sample_configuration(config_levels, size)
