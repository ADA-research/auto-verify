from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, ContextManager

from ConfigSpace import Categorical, ConfigurationSpace, Float

from autoverify.verifier.verification_result import VerificationResultString
from autoverify.verifier.verifier import CompleteVerifier

dummy_configspace = ConfigurationSpace()
dummy_configspace.add_hyperparameters(
    [
        Float("x", (0.0, 10.0), default=5.0),
        Float("xx", (0.0, 10.0), default=9.0),
        Float("xy", (0.0, 10.0), default=2.0),
        Float("y", (0.0, 10.0)),
    ]
)


class DummyVerifier(CompleteVerifier):
    name: str = "dummy"
    config_space: ConfigurationSpace = dummy_configspace

    @property
    def contexts(self) -> list[ContextManager[None]] | None:
        return None

    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: Any,
    ) -> tuple[str, Path | None]:
        return (f"sleep {config['x'] / 10}", None)

    def _parse_result(
        self,
        sp_result: CompletedProcess[bytes] | None,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        return "UNSAT", None

    def _init_config(self, network: Path, property: Path, config: Any) -> Any:
        return config
