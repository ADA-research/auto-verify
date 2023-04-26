"""ab-crown verifier."""
import os
import subprocess
from pathlib import Path

from result import Err, Ok

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
        os.chdir(self.tool_path / "complete_verifier")
        yaml_config = simple_abcrown_config(property, network)
        run_cmd = self._get_runner_cmd(Path(yaml_config.name))
        print("-" * 80)
        print(run_cmd)
        print("-" * 80)
        try:
            result = subprocess.run(
                run_cmd,
                executable="/bin/bash",
                capture_output=True,
                check=True,
                shell=True,
            )
        except Exception as err:
            print(f"Exception during call to abcrown, {err}")
            return Err("Exception during call to abcrown")

        stdout = result.stdout.decode()
        print("=" * 80)
        print(stdout)
        print("=" * 80)

        return Ok(CompleteVerificationOutcome("SAT", ("a", "a")))

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return

    def _get_runner_cmd(self, abcrown_config: Path) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python abcrown.py --config {str(abcrown_config)}
        """
