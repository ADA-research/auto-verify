"""TODO docstring."""
import subprocess
import time
from abc import ABC, abstractmethod
from contextlib import ExitStack
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, ContextManager

from ConfigSpace import Configuration, ConfigurationSpace
from result import Err, Ok

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.cli.install import TOOL_DIR_NAME, VERIFIER_DIR
from autoverify.util.conda import get_verifier_conda_env_name
from autoverify.util.path import check_file_extension
from autoverify.verifier.verification_result import (
    CompleteVerificationData,
    CompleteVerificationResult,
    VerificationResultString,
)


class Verifier(ABC):
    """Abstract class to represent a verifier tool."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique verifier name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def config_space(self) -> ConfigurationSpace:
        """Configuration space to sample from."""
        raise NotImplementedError

    @property
    @abstractmethod
    def contexts(self) -> list[ContextManager[None]] | None:
        """Contexts to run the verification in."""
        raise NotImplementedError

    @property
    def tool_path(self) -> Path:
        """The path where the verifier is installed."""
        tool_path = VERIFIER_DIR / self.name / TOOL_DIR_NAME

        if not tool_path.exists():
            raise FileNotFoundError(
                f"Could not find installation for tool {self.name}"
            )

        return Path(tool_path)  # mypy complains tool_path is any

    @property
    def conda_env_name(self) -> str:
        """The conda environment name associated with the verifier."""
        return get_verifier_conda_env_name(self.name)

    @property
    def default_config(self) -> Configuration:
        """Return the default configuration of the config level."""
        return self.config_space.get_default_configuration()

    @abstractmethod
    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: Any,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> tuple[str, Path | None]:
        """_summary_."""
        raise NotImplementedError

    @abstractmethod
    def _parse_result(
        self,
        sp_result: CompletedProcess[bytes] | None,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        """_summary."""
        raise NotImplementedError

    @abstractmethod
    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Any,
    ) -> Any:
        """_summary."""
        raise NotImplementedError

    def sample_configuration(
        self, *, size: int = 1
    ) -> Configuration | list[Configuration]:
        """Sample one or more configurations.

        Args:
            size: The number of configurations to sample.

        Returns:
            Configuration | list[Configuration]: The sampled configurations.
        """
        return self.config_space.sample_configuration(size=size)

    @staticmethod
    def is_same_config(config1: Any, config2: Any) -> bool:
        """Check if a config is the same as the self config."""
        raise NotImplementedError


class CompleteVerifier(Verifier):
    """_summary_."""

    def verify_property(
        self,
        network: Path,
        property: Path,
        *,
        config: Configuration | Path | None = None,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> CompleteVerificationResult:
        """Verify the property on the network.

        Runs the verifier and feeds the network/property instance as input.
        Complete verification will result in one of the following three
        possibilities: `SAT`, `UNSAT`, `TIMEOUT`.

        Args:
            network: The `Path` to the network in `.onnx` format.
            property: The `Path` to the property in `.vnnlib` format.
            config: The configuration of the verification tool to be used. If
                `None` is passed, the default configuration of the verification
                tool will be used.
            timeout: The maximum number of seconds that can be spent on the
                verification query.

        Returns:
            CompleteVerificationResult: A `Result` object containing information
                about the verification attempt. TODO: Link docs or something
        """
        if not check_file_extension(network, ".onnx"):
            raise ValueError("Network should be in onnx format")

        if not check_file_extension(property, ".vnnlib"):
            raise ValueError("Property should be in vnnlib format")

        if config is None:
            config = self.default_config

        # Tools use different configuration formats and methods, thus we let
        # them do some initialization here
        config = self._init_config(network, property, config)

        run_cmd, output_file = self._get_run_cmd(
            network, property, config=config, timeout=timeout
        )

        outcome = self._run_verification(
            run_cmd,
            result_file=output_file,
            timeout=timeout,
        )

        # Shutting down after timeout may take some time, so we set the took
        # value to the actual timeout
        if outcome.result == "TIMEOUT":
            outcome.took = timeout

        if outcome.err == "":  # TODO: Makes more sense if we set err to None
            return Ok(outcome)
        else:
            return Err(outcome)

    def _run_verification(
        self,
        run_cmd: str,
        *,
        result_file: Path | None = None,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> CompleteVerificationData:
        """_summary_."""
        before_t = time.time()
        result: VerificationResultString | None = None
        counter_example: str | None = None
        sp_result: CompletedProcess[bytes] | None = None
        run_err: str = ""

        try:
            contexts = self.contexts or []

            with ExitStack() as stack:
                for context in contexts:
                    stack.enter_context(context)

                sp_result = subprocess.run(
                    run_cmd,
                    executable="/bin/bash",
                    capture_output=True,
                    check=True,
                    shell=True,
                    timeout=timeout,
                )
        except subprocess.TimeoutExpired:
            took_t = time.time() - before_t
            result = "TIMEOUT"
        except Exception as err:
            took_t = time.time() - before_t
            result = "ERR"
            run_err = f"Exception during verification:\n {err}"
        else:
            took_t = time.time() - before_t

        if result is None:
            result, counter_example = self._parse_result(sp_result, result_file)

        return CompleteVerificationData(
            result,
            took_t,
            counter_example,
            run_err,
        )
