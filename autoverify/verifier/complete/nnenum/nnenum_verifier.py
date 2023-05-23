"""Nnenum verifier."""
import sys
import tempfile
from pathlib import Path
from subprocess import CompletedProcess
from typing import ContextManager

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, environment
from autoverify.util.loggers import verification_logger
from autoverify.util.proc import cpu_count
from autoverify.verifier.verification_result import VerificationResultString
from autoverify.verifier.verifier import CompleteVerifier

from .nnenum_configspace import NnenumConfigspace


class Nnenum(CompleteVerifier):
    """_summary_."""

    name: str = "nnenum"
    config_space: ConfigurationSpace = NnenumConfigspace

    @property
    def contexts(self) -> list[ContextManager[None]]:
        return [
            cwd(self.tool_path / "src"),
            environment(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"),
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
        config: str,
    ) -> tuple[str, Path | None]:
        result_file = Path(tempfile.NamedTemporaryFile("w").name)
        source_cmd = get_conda_source_cmd(get_conda_path())

        # The timeout is handled by subprocess.run, so its set it to maxint here
        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python -m nnenum.nnenum {str(network)} {str(property)} {sys.maxsize} \
        {str(result_file)} \
        {str(cpu_count())} \
        {config}
        """

        return run_cmd, result_file

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | str | None,
    ) -> str:
        if config is None:
            return str(self.default_config["settings_mode"])

        if isinstance(config, Configuration):
            return str(config["settings_mode"])  # type: ignore
        elif isinstance(config, str):
            return config

        verification_logger.warning("Invalid nnenum config, using default.")

        return str(self.default_config["settings_mode"])
