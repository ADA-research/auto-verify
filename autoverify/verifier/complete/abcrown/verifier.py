"""ab-crown verifier."""
from collections.abc import Iterable
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, ContextManager

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, pkill_matches
from autoverify.util.tempfiles import tmp_file
from autoverify.verifier.complete.abcrown.abcrown_yaml_config import (
    AbcrownYamlConfig,
)
from autoverify.verifier.complete.abcrown.configspace import AbCrownConfigspace
from autoverify.verifier.verification_result import (
    CompleteVerificationResult,
    VerificationResultString,
)
from autoverify.verifier.verifier import CompleteVerifier


class AbCrown(CompleteVerifier):
    """_summary_."""

    name: str = "abcrown"
    config_space: ConfigurationSpace = AbCrownConfigspace

    @property
    def contexts(self) -> list[ContextManager[None]]:
        # TODO: Narrow the pkill_match_list patterns further. People may be
        # running scripts called 'abcrown.py'
        return [
            cwd(self.tool_path / "complete_verifier"),
            pkill_matches(["python abcrown.py"]),
        ]

    def _parse_result(
        self,
        sp_result: CompletedProcess[bytes] | None,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        tool_result = ""

        if sp_result is not None:
            tool_result = sp_result.stdout.decode()

        if find_substring("Result: sat", tool_result):
            with open(str(result_file), "r") as f:
                counter_example = f.read()

            return "SAT", counter_example
        elif find_substring("Result: unsat", tool_result):
            return "UNSAT", None
        elif find_substring("Result: timeout", tool_result):
            return "TIMEOUT", None

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
        python abcrown.py --config {str(config)} \
        --results_file {str(result_file)} \
        --timeout {str(timeout)}
        """

        return run_cmd, result_file

    def _verify_batch(
        self,
        instances: Iterable[Any],
        *,
        config: Configuration | Path | None,
    ) -> list[CompleteVerificationResult]:
        source_cmd = get_conda_source_cmd()
        # TODO:

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | Path,
    ) -> Path:
        if isinstance(config, Configuration):
            yaml_config = AbcrownYamlConfig.from_config(
                config, network, property, batch_size=self._batch_size
            )
        elif isinstance(config, Path):
            yaml_config = AbcrownYamlConfig.from_yaml(
                config, network, property, batch_size=self._batch_size
            )
        else:
            raise ValueError("Config should be a Configuration or Path")

        return Path(yaml_config.get_yaml_file_path())
