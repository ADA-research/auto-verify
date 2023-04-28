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

from .nnenum_configspace import NnenumConfigspace


class Nnenum(CompleteVerifier):
    """_summary_."""

    name: str = "nnenum"
    verifier_configspace: VerifierConfigurationSpace = NnenumConfigspace

    # TODO: Configspace
    # kwarg for cfgspace?
    # set an optional default cfgspace attr?
    def verify_property(
        self, property: Path, network: Path
    ) -> CompleteVerificationResult:
        """_summary_."""
        os.chdir(self.tool_path / "src")

        with environment(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"):
            run_cmd = self._get_runner_cmd(property, network)

            try:
                result = subprocess.run(
                    run_cmd,
                    executable="/bin/bash",
                    capture_output=True,
                    check=True,
                    shell=True,
                )
            except subprocess.CalledProcessError as err:
                print(f"nnenum Error:\n{err.stderr}")
                return Err("Exception during call to nnenum")
            except Exception as err:
                print(f"Exception during call to nnenum, {err=}")
                return Err("Exception during call to nnenum")

        stdout = result.stdout.decode()
        verification_outcome = self._parse_result(stdout)

        if isinstance(verification_outcome, CompleteVerificationOutcome):
            return Ok(verification_outcome)
        else:
            return Err("Failed to parse output")

    def _parse_result(
        self, tool_result: str
    ) -> CompleteVerificationOutcome | None:
        if find_substring("UNSAFE", tool_result):
            counter_example = self._parse_counter_example(tool_result)
            return CompleteVerificationOutcome("SAT", counter_example)
        elif find_substring("SAFE", tool_result):
            return CompleteVerificationOutcome("UNSAT")

        return None

    # TODO: A standard for counterexamples was defined in vnncomp2022
    # https://github.com/stanleybak/vnncomp2022/issues/1#issuecomment-1074022041
    def _parse_counter_example(self, tool_output: str) -> tuple[str, str]:
        counter_input: str = ""
        counter_output: str = ""

        tool_output_lines = tool_output.splitlines()

        for i, line in enumerate(tool_output_lines):
            if line.startswith("Result:"):
                input_line = tool_output_lines[i + 1]
                output_line = tool_output_lines[i + 2]

                counter_input = input_line.split(maxsplit=1)[1]
                counter_output = output_line.split(maxsplit=1)[1]

        return counter_input, counter_output

    def _get_runner_cmd(self, property: Path, network: Path) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python -m nnenum.nnenum {str(network)} {str(property)}
        """

    # TODO:
    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        """_summary_."""
        return super().sample_configuration(config_levels, size)
