"""ab-crown verifier."""
import os
import subprocess
import tempfile
from pathlib import Path

from result import Err, Ok

from autoverify.util import find_substring
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
        result_file = Path(tempfile.NamedTemporaryFile("w").name)

        run_cmd = self._get_runner_cmd(Path(yaml_config.name), result_file)

        try:
            result = subprocess.run(
                run_cmd,
                executable="/bin/bash",
                capture_output=True,
                check=True,
                shell=True,
            )
        except subprocess.CalledProcessError as err:
            print(f"AbCrown Error:\n{err.stderr}")
            return Err("Exception during call to ab-crown")
        except Exception as err:
            print(f"Exception during call to ab-crown, {str(err)}")
            return Err("Exception during call to ab-crown")

        # TODO: Parse counterexample
        stdout = result.stdout.decode()
        verification_outcome = self._parse_result(stdout, result_file)

        if isinstance(verification_outcome, CompleteVerificationOutcome):
            return Ok(verification_outcome)
        else:
            return Err("Failed to parse output")

    def _parse_result(
        self,
        tool_result: str,
        result_file: Path,
    ) -> CompleteVerificationOutcome | None:
        """_summary_."""
        if find_substring("Result: sat", tool_result):
            return CompleteVerificationOutcome("SAT", result_file.read_text())
        elif find_substring("Result: unsat", tool_result):
            return CompleteVerificationOutcome("UNSAT", None)

        return None

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return

    def _get_runner_cmd(self, abcrown_config: Path, result_file: Path) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python abcrown.py --config {str(abcrown_config)} \
        --results_file {str(result_file)}
        """
