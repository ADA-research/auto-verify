"""Nnenum verifier."""
# TODO: More links and details in above docstring
import os
import subprocess
from pathlib import Path

from result import Err, Ok

from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import environment
from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
)
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)

from .mnbab_configspace import MnBabConfigspace


class MnBab(CompleteVerifier):
    """_summary_."""

    name: str = "mnbab"
    verifier_configspace: VerifierConfigurationSpace = MnBabConfigspace

    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        """_summary_."""
        # TODO:
        return Ok(CompleteVerificationOutcome("UNSAT"))

    # TODO:
    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return super().sample_configuration(config_levels, size)
