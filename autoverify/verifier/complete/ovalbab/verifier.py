"""OvalBab verifier."""
from pathlib import Path
from subprocess import CompletedProcess
from typing import ContextManager

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd
from autoverify.util.tempfiles import tmp_file
from autoverify.verifier.complete.ovalbab.ovalbab_json_config import (
    OvalbabJsonConfig,
)
from autoverify.verifier.verification_result import VerificationResultString
from autoverify.verifier.verifier import CompleteVerifier

from .configspace import OvalBabConfigspace


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
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> tuple[str, Path | None]:
        result_file = Path(tmp_file(".txt").name)
        source_cmd = get_conda_source_cmd(get_conda_path())

        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python tools/bab_tools/bab_from_vnnlib.py --mode run_instance \
        --onnx {str(network)} \
        --vnnlib {str(property)} \
        --result_file {str(result_file)} \
        --json {str(config)} \
        --instance_timeout {timeout}
        """

        return run_cmd, result_file

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | Path,
    ) -> Path:
        if isinstance(config, Configuration):
            json_config = OvalbabJsonConfig.from_config(config)
        elif isinstance(config, Path):
            json_config = OvalbabJsonConfig.from_json(config)
        else:
            raise ValueError("Config should be a Configuration, Path or None")

        return Path(json_config.get_json_file_path())
