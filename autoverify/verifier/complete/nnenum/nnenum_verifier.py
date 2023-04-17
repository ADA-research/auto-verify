"""Nnenum verifier."""
# TODO: More links and details in above docstring
import os
import subprocess
from pathlib import Path

from result import Err, Ok

from autoverify.util import find_substring
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

    # TODO: Counterexamples
    # TODO: Error handling
    # TODO: Modular way of sourcing conda env
    # TODO: Modular way to determine conda.sh path
    # TODO: Use a contextmanager for exporting env vars
    # TODO: Configspace
    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        """_summary_."""
        os.chdir(self.tool_path / "src")
        result = subprocess.run(
            f"""
            source ~/miniconda3/etc/profile.d/conda.sh
            conda activate __av__nnenum
            export OPENBLAS_NUM_THREADS=1
            export OMP_NUM_THREADS=1
            python -m nnenum.nnenum {str(network)} {str(property)}
            """,
            executable="/bin/bash",
            capture_output=True,
            shell=True,
        )
        stdout = result.stdout.decode("utf-8")
        # stderr = result.stderr.decode("utf-8")

        if find_substring("UNSAFE", stdout):
            return Ok(CompleteVerificationOutcome("SAT", None))
        elif find_substring("SAFE", stdout):
            return Ok(CompleteVerificationOutcome("UNSAT", None))

        return Err("Uhm???")

    # TODO:
    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return super().sample_configuration(config_levels, size)
