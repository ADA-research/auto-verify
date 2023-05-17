"""TODO docstring."""
from abc import ABC, abstractmethod
from pathlib import Path

from ConfigSpace import Configuration, ConfigurationSpace
from result import Err, Ok

from autoverify.cli.install import TOOL_DIR_NAME, VERIFIER_DIR
from autoverify.util.conda import get_verifier_conda_env_name
from autoverify.util.path import check_file_extension
from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
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


class CompleteVerifier(Verifier):
    """_summary_."""

    def verify_property(
        self,
        network: Path,
        property: Path,
        *,
        config: Configuration | None = None,
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

        outcome = self._verify_property(network, property, config=config)

        if isinstance(outcome, CompleteVerificationOutcome):
            return Ok(outcome)
        else:
            return outcome  # Err

    @abstractmethod
    def _verify_property(
        self,
        network: Path,
        property: Path,
        *,
        config: Configuration = None,
    ) -> CompleteVerificationOutcome | Err[str]:
        """_summary_."""
        raise NotImplementedError
