"""Temporary dummy verifier."""
from pathlib import Path

from ConfigSpace import Configuration, ConfigurationSpace
from result import Err

from autoverify.verifier.verification_result import CompleteVerificationOutcome
from autoverify.verifier.verifier import CompleteVerifier

from .dummy_configspace import DummyConfigspace


class DummyVerifier(CompleteVerifier):
    """_summary_."""

    name: str = "DummyVerifier"
    config_space: ConfigurationSpace = DummyConfigspace

    def _verify_property(
        self,
        network: Path,
        property: Path,
        *,
        config: Configuration | Path | None = None,
    ) -> CompleteVerificationOutcome | Err[str]:
        """_summary_."""
        # temp silence warnings
        property, network = network, property

        return CompleteVerificationOutcome("SAT", None)
