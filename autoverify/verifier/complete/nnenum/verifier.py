"""Nnenum verifier."""
import shlex
import tempfile
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, ContextManager

import numpy as np
from ConfigSpace import Configuration, ConfigurationSpace

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, environment, pkill_matches
from autoverify.util.loggers import verification_logger
from autoverify.util.proc import cpu_count, pkill_match
from autoverify.verifier.verification_result import VerificationResultString
from autoverify.verifier.verifier import CompleteVerifier

from .configspace import NnenumConfigspace


class Nnenum(CompleteVerifier):
    """_summary_."""

    name: str = "nnenum"
    config_space: ConfigurationSpace = NnenumConfigspace

    @property
    def contexts(self) -> list[ContextManager[None]]:
        return [
            cwd(self.tool_path / "src"),
            environment(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"),
            pkill_matches(["python -m nnenum.nnenum"]),
        ]

    def _parse_result(
        self,
        _: CompletedProcess[bytes] | None,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        with open(str(result_file), "r") as f:
            result_txt = f.read()

        first_line = result_txt.split("\n", maxsplit=1)[0]

        if first_line == "unsat":
            return "UNSAT", None
        elif first_line == "sat":
            counter_example = self._parse_counter_example(result_txt)
            return "SAT", counter_example
        elif first_line == "timeout":
            return "TIMEOUT", None

        return "ERR", None

    def _parse_counter_example(self, result_txt: str) -> str:
        return result_txt.split("\n", maxsplit=1)[1]

    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: dict[str, Any],
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> tuple[str, Path | None]:
        result_file = Path(tempfile.NamedTemporaryFile("w").name)
        source_cmd = get_conda_source_cmd(get_conda_path())

        # The timeout is handled by subprocess.run, so its set it to maxint here
        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python -m nnenum.nnenum {str(network)} {str(property)} {str(timeout)} \
        {str(result_file)} \
        {str(cpu_count())} \
        {shlex.quote(str(config))} \
        """

        return run_cmd, result_file

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | Path,
    ) -> dict[str, Any]:
        if not isinstance(config, Configuration):
            raise ValueError("Configuration files for nnenum not supported yet")

        dict_config = dict(config)

        if dict_config["INF_OVERAPPROX_MIN_GEN_LIMIT"] is True:
            dict_config["OVERAPPROX_MIN_GEN_LIMIT"] = np.inf

        if dict_config["INF_OVERAPPROX_LP_TIMEOUT"] is True:
            dict_config["OVERAPPROX_LP_TIMEOUT"] = np.inf

        del dict_config["INF_OVERAPPROX_LP_TIMEOUT"]
        del dict_config["INF_OVERAPPROX_MIN_GEN_LIMIT"]

        return dict_config

    @staticmethod
    def is_same_config(
        config1: Configuration | str, config2: Configuration | str
    ) -> bool:
        if isinstance(config1, Configuration):
            config1 = str(config1["settings_mode"])  # type: ignore
        if isinstance(config2, Configuration):
            config2 = str(config2["settings_mode"])  # type: ignore

        return config1 == config2
