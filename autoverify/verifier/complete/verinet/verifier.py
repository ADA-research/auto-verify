import shlex
from pathlib import Path
from subprocess import CompletedProcess
from typing import ContextManager

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, environment, pkill_matches
from autoverify.util.onnx import get_input_shape
from autoverify.verifier.verification_result import VerificationResultString
from autoverify.verifier.verifier import CompleteVerifier

from .configspace import VerinetConfigspace


# TODO: Warn user that `batch_size` init param is not used by Verinet atm
class Verinet(CompleteVerifier):
    """_summary_."""

    name: str = "verinet"
    config_space: ConfigurationSpace = VerinetConfigspace

    @property
    def contexts(self) -> list[ContextManager[None]]:
        return [
            cwd(self.tool_path),
            environment(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"),
            pkill_matches(
                [
                    "multiprocessing.spawn",
                    "multiprocessing.forkserver",
                    "python cli.py",  # TODO: Too broad
                ]
            ),
        ]

    def _parse_result(
        self,
        sp_result: CompletedProcess[bytes] | None,
        _: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        tool_result = ""

        if sp_result is not None:
            tool_result = sp_result.stdout.decode()

        if find_substring("STATUS:  Status.Safe", tool_result):
            return "UNSAT", None
        elif find_substring("STATUS:  Status.Unsafe", tool_result):
            return "SAT", None
        elif find_substring("STATUS:  Status.Undecided", tool_result):
            return "TIMEOUT", None

        return "ERR", None

    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: Configuration,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> tuple[str, Path | None]:
        source_cmd = get_conda_source_cmd(get_conda_path())
        input_shape = get_input_shape(network)

        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python cli.py {str(network)} {str(property)} {timeout} \
        {shlex.quote(str(dict(config)))} \
        {shlex.quote(str(input_shape))} \
        {-1} \
        {True} \
        """

        return run_cmd, None
