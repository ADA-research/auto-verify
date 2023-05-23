"""OvalBab verifier."""
import sys
import tempfile
from pathlib import Path
from subprocess import CompletedProcess
from typing import ContextManager

from ConfigSpace import ConfigurationSpace

from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, get_file_path
from autoverify.verifier.verification_result import VerificationResultString
from autoverify.verifier.verifier import CompleteVerifier

from .ovalbab_configspace import OvalBabConfigspace


class OvalBab(CompleteVerifier):
    """_summary_."""

    name: str = "ovalbab"
    config_space: ConfigurationSpace = OvalBabConfigspace

    @property
    def contexts(self) -> list[ContextManager[None]]:
        return [cwd(self.tool_path)]

    def _parse_result(
        self,
        _: CompletedProcess[bytes] | None,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        with open(str(result_file), "r") as f:
            result_text = f.read()

        if find_substring("violated", result_text):
            # TODO: Counterexample (not sure if its saved at all by ovalbab?)
            return "SAT", None
        elif find_substring("holds", result_text):
            return "UNSAT", None

        return "ERR", None

    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: Path,
    ) -> tuple[str, Path | None]:
        result_file = Path(tempfile.NamedTemporaryFile("w").name)
        # TODO: Real Configs
        config_file = get_file_path(Path(__file__)) / "temp_ovalbab_config.json"
        source_cmd = get_conda_source_cmd(get_conda_path())

        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python tools/bab_tools/bab_from_vnnlib.py --mode run_instance \
        --onnx {str(network)} \
        --vnnlib {str(property)} \
        --result_file {str(result_file)} \
        --json {config_file} \
        --instance_timeout {sys.maxsize}
        """

        return run_cmd, result_file

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Path,
    ) -> Path:
        # TODO:
        return config
