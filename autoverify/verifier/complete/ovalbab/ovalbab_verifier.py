"""OvalBab verifier."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from result import Err, Ok

from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import get_file_path
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
        os.chdir(self.tool_path)

        result_file = Path(tempfile.NamedTemporaryFile("w").name)
        config_file = get_file_path(Path(__file__)) / "temp_ovalbab_config.json"

        run_cmd = self._get_runner_cmd(
            property, network, result_file, config_file
        )

        try:
            result = subprocess.run(
                run_cmd,
                executable="/bin/bash",
                capture_output=True,
                check=True,
                shell=True,
            )
        except subprocess.CalledProcessError as err:
            print(f"OvalBab Error:\n{err.stderr}")
            return Err("Exception during call to oval-bab")
        except Exception as err:
            print(f"Exception during call to oval-bab, {str(err)}")
            return Err("Exception during call to oval-bab")

        stdout = result.stdout.decode()
        print(stdout)
        verification_outcome = self._parse_result(result_file)

        if isinstance(verification_outcome, CompleteVerificationOutcome):
            return Ok(verification_outcome)
        else:
            return Err("Failed to parse output")

    def _parse_result(
        self,
        result_file: Path,
    ) -> CompleteVerificationOutcome | None:
        """_summary_."""
        result_text = result_file.read_text()

        if find_substring("violated", result_text):
            # TODO: Counterexample
            return CompleteVerificationOutcome("SAT", None)
        elif find_substring("holds", result_text):
            return CompleteVerificationOutcome("UNSAT")

        return None

    def _get_runner_cmd(
        self,
        property: Path,
        network: Path,
        result_file: Path,
        config_file: Path,
    ) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python tools/bab_tools/bab_from_vnnlib.py --mode run_instance \
        --onnx {str(network)} --vnnlib {str(property)} \
        --result_file {str(result_file)} --json {config_file} \
        --instance_timeout {sys.maxsize}
        """

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return super().sample_configuration(config_levels, size)
