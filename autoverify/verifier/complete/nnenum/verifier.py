"""Nnenum verifier."""
import shlex
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, ContextManager, Iterable

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, environment, pkill_matches
from autoverify.util.proc import cpu_count
from autoverify.util.tempfiles import tmp_file
from autoverify.verifier.verification_result import (
    CompleteVerificationResult,
    VerificationResultString,
)
from autoverify.verifier.verifier import CompleteVerifier

from .configspace import NnenumConfigspace


class Nnenum(CompleteVerifier):
    """_summary_."""

    name: str = "nnenum"
    config_space: ConfigurationSpace = NnenumConfigspace

    # HACK: Should not need to instantiate a whole new instance just to
    # change `_use_auto_settings`.
    def __init__(self, batch_size: int = 512, use_auto_settings: bool = False):
        """_summary_."""
        super().__init__(batch_size)
        self._use_auto_settings = use_auto_settings

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
        result_file = Path(tmp_file(".txt").name)
        source_cmd = get_conda_source_cmd(get_conda_path())

        # In nnenum, settings are normally passed as a one word string
        # over the CLI. This word then selects from some pre-defined settings
        # We want some more control however, so we also make an option to pass
        # a stringified dict of exact settings.
        # The "none" value for settings_str is used as a flag that makes
        # nnenum use the dict of exact settings instead.
        settings_str = "none"
        if self._use_auto_settings:
            settings_str = "auto"  # "auto" is the default
            config = {}

        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python -m nnenum.nnenum {str(network)} {str(property)} {str(timeout)} \
        {str(result_file)} \
        {str(cpu_count())} \
        {settings_str} \
        {shlex.quote(str(config))} \
        """

        return run_cmd, result_file

    def _verify_batch(
        self,
        instances: Iterable[Any],
        *,
        config: Configuration | Path | None,
    ) -> list[CompleteVerificationResult]:
        # source_cmd = get_conda_source_cmd()
        # TODO:
        raise NotImplementedError("Batch verification not supported yet")

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | Path,
    ) -> dict[str, Any]:
        if isinstance(config, Path):
            raise ValueError("Configuration files for nnenum not supported yet")

        import copy

        dict_config = copy.deepcopy(dict(config))

        # HACK: Cant safely evaluate `np.inf`, instead we pass it as a string
        # that is converted back to `np.inf` in the nnenum code.
        # if dict_config["INF_OVERAPPROX_MIN_GEN_LIMIT"] is True:
        #     dict_config["OVERAPPROX_MIN_GEN_LIMIT"] = "_inf"
        #
        # if dict_config["INF_OVERAPPROX_LP_TIMEOUT"] is True:
        #     dict_config["OVERAPPROX_LP_TIMEOUT"] = "_inf"
        #
        # del dict_config["INF_OVERAPPROX_LP_TIMEOUT"]
        # del dict_config["INF_OVERAPPROX_MIN_GEN_LIMIT"]

        return dict_config

    @staticmethod
    def is_same_config(
        config1: Configuration | str, config2: Configuration | str
    ) -> bool:
        """_summary_."""
        if isinstance(config1, Configuration):
            config1 = str(config1["settings_mode"])  # type: ignore
        if isinstance(config2, Configuration):
            config2 = str(config2["settings_mode"])  # type: ignore

        return config1 == config2
