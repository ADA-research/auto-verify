"""ab-crown verifier."""
from pathlib import Path
from typing import IO

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

from .abcrown_yaml_generator import simple_abcrown_config


class AbCrown(CompleteVerifier):
    """_summary_."""

    name: str = "abcrown"
    verifier_configspace: VerifierConfigurationSpace = AbCrownConfigspace

    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        """_summary_."""
        yaml_config = simple_abcrown_config(property, network)
        with open(yaml_config, "r") as f:
            print(yaml_config.read())
        return Ok(CompleteVerificationOutcome("SAT", ("a", "a")))

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
