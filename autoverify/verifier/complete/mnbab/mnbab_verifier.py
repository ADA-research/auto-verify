"""Nnenum verifier."""
# TODO: More links and details in above docstring
import os

# import subprocess
from pathlib import Path

from ConfigSpace import Configuration, ConfigurationSpace
from result import Err, Ok

# from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd

# from autoverify.util.env import environment
from autoverify.verifier.verification_result import CompleteVerificationOutcome
from autoverify.verifier.verifier import CompleteVerifier

from .mnbab_configspace import MnBabConfigspace


class MnBab(CompleteVerifier):
    """_summary_."""

    name: str = "mnbab"
    config_space: ConfigurationSpace = MnBabConfigspace

    def _verify_property(
        self,
        network: Path,
        property: Path,
        *,
        config: Configuration | Path | None = None,
    ) -> CompleteVerificationOutcome | Err:
        """_summary_."""
        # TODO: Mnbab runner
        os.chdir(self.tool_path)
        # run_cmd = self._get_runner_cmd(), result_file)

        return CompleteVerificationOutcome("UNSAT")

    def _get_runner_cmd(self, mnbab_config: Path) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python src/vnncomp_runner.py -c {str(mnbab_config)}
        """
