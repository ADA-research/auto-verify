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

from .nnenum_configspace import DummyConfigspace


class Nnenum(CompleteVerifier):
    """_summary_."""

    name: str = "nnenum"
    verifier_configspace: VerifierConfigurationSpace = DummyConfigspace

    # TODO: Counterexamples
    # TODO: Error handling
    # TODO: Configspace
    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        """_summary_."""
        os.chdir(self.tool_path / "src")

        with environment(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"):
            run_cmd = self._get_runner_cmd(property, network)

            result = subprocess.run(
                run_cmd,
                executable="/bin/bash",
                capture_output=True,
                check=True,
                shell=True,
            )

        stdout = result.stdout.decode()
        # stderr = result.stderr.decode()

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

    def _get_runner_cmd(self, property: Path, network: Path) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python -m nnenum.nnenum {str(network)} {str(property)}
        """
