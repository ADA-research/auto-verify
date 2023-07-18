"""Nnenum verifier."""
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import ContextManager

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, environment
from autoverify.verifier.complete.mnbab.mnbab_json import MnbabJsonConfig
from autoverify.verifier.verification_result import VerificationResultString
from autoverify.verifier.verifier import CompleteVerifier

from .configspace import MnBabConfigspace


class MnBab(CompleteVerifier):
    """MnBab verifier."""

    name: str = "mnbab"
    config_space: ConfigurationSpace = MnBabConfigspace

    def test(self):
        source_cmd = get_conda_source_cmd(get_conda_path())
        env_lib_path = get_conda_path() / "envs" / self.conda_env_name / "lib"

        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        export PYTHONPATH=$PYTHONPATH:$PWD
        python src/run_instance.py
        """

        with cwd(self.tool_path), environment(
            LD_LIBRARY_PATH=str(env_lib_path)
        ):
            subprocess.run(run_cmd, executable="/bin/bash", shell=True)

    @property
    def contexts(self) -> list[ContextManager[None]]:
        env_lib_path = get_conda_path() / "envs" / self.conda_env_name / "lib"

        return [
            cwd(self.tool_path),
            environment(LD_LIBRARY_PATH=str(env_lib_path)),
        ]

    def _parse_result(
        self,
        sp_result: CompletedProcess[bytes] | None,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        # TODO:
        return "SAT", None

    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: Path,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> tuple[str, Path | None]:
        source_cmd = get_conda_source_cmd(get_conda_path())

        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        export PYTHONPATH=$PYTHONPATH:$PWD
        python src/utilities/prepare_instance.py \\
        -b mnbabtest \\
        -n {str(network)} \\
        -s {str(property)} \\
        """

        # -r {Path("/home/c/thesis/auto-verify/mn_out/")} \\
        # -t {timeout}
        return run_cmd, None

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | Path,
        *,
        batch_size: int | None = None,
    ) -> Path:
        if isinstance(config, Configuration):
            json_config = MnbabJsonConfig.from_config(config, network, property)
        elif isinstance(config, Path):
            json_config = MnbabJsonConfig.from_json(config, network, property)
        else:
            raise ValueError("Config should be a Configuration, Path or None")

        return Path(json_config.get_json_file_path())
