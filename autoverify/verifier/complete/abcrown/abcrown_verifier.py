"""ab-crown verifier."""
import os
import tempfile
from pathlib import Path
from typing import IO

import yaml
from result import Ok

from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.verifier.complete.abcrown.abcrown_configspace import (
    AbCrownConfigspace,
)
from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
)
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)


class AbCrown(CompleteVerifier):
    """_summary_."""

    name: str = "abcrown"
    verifier_configspace: VerifierConfigurationSpace = AbCrownConfigspace

    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        """_summary_."""
        yaml_file = self.make_minimal_abcrown_config(property, network)
        print(yaml_file)
        # return Ok(CompleteVerificationOutcome("SAT", ("a", "a")))

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return

    def _get_runner_cmd(self, property: Path, network: Path) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python -m nnenum.nnenum {str(network)} {str(property)}
        """

    @staticmethod
    def make_minimal_abcrown_config(prop: Path, network: Path) -> IO[bytes]:
        """Creates a barebones .yaml config for 1 onnx and 1 vnnlib."""
        yaml_file = tempfile.TemporaryFile(suffix="yaml")

        yaml.dump({"a": 1}, yaml_file)

        return yaml_file
