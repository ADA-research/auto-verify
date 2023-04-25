"""ab-crown verifier"""
from pathlib import Path

from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)


class AbCrown(CompleteVerifier):
    """_summary_."""

    name: str = "ab-crown"
    verifier_configspace: VerifierConfigurationSpace

    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        return super().verify_property(property, network)

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        return super().sample_configuration(config_levels, size)
