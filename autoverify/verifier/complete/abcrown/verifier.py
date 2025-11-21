"""Ab-crown verifier."""

from collections.abc import Iterable
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any

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
    """AB-Crown."""

    name: str = "abcrown"
    config_space: ConfigurationSpace = AbCrownConfigspace

    def __init__(
        self,
        batch_size: int = 512,
        cpu_gpu_allocation: tuple[int, int, int] | None = None,
        yaml_override: dict[str, Any] | None = None,
    ):
        """New instance."""
        if cpu_gpu_allocation and cpu_gpu_allocation[2] < 0:
            raise ValueError("AB-Crown CPU only mode not yet supported")

        super().__init__(batch_size, cpu_gpu_allocation)
        self._yaml_override = yaml_override

    @property
    def contexts(self) -> list[AbstractContextManager[None]]:
        # TODO: Narrow the pkill_match_list patterns further. People may be
        # running scripts called 'abcrown.py'
        # Ideally just keep track of PIDs rather than pkill name matching
        return [
            cwd(self.tool_path / "complete_verifier"),
            pkill_matches(["python abcrown.py"]),
        ]

    def _parse_result(
        self,
        output: str,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        if find_substring("Result: sat", output):
            with open(str(result_file)) as f:
                counter_example = f.read()

            return "SAT", counter_example
        elif find_substring("Result: unsat", output):
            return "UNSAT", None
        elif find_substring("Result: timeout", output):
            return "TIMEOUT", None

        return "TIMEOUT", None

    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: Path,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> tuple[str, Path | None]:
        with tmp_file(".txt") as tmp:
            result_file = Path(tmp.name)
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
        # source_cmd = get_conda_source_cmd()
        # TODO:
        raise NotImplementedError("Batch verification not supported yet")

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | Path,
    ) -> Path:
        if isinstance(config, Configuration):
            yaml_config = AbcrownYamlConfig.from_config(
                config,
                network,
                property,
                batch_size=self._batch_size,
                yaml_override=self._yaml_override,
            )
        else: # isinstance(config, Path)
            yaml_config = AbcrownYamlConfig.from_yaml(
                config,
                network,
                property,
                batch_size=self._batch_size,
                yaml_override=self._yaml_override,
            )
        
        return Path(yaml_config.get_yaml_file_path())
