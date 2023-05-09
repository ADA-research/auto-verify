"""_summary_."""
import time
from pathlib import Path
from typing import Type

from ConfigSpace import Configuration
from result import Ok

from autoverify.verifier.verifier import CompleteVerifier


def make_verifier_target_function(
    verifier: Type[CompleteVerifier],
    timeout_penalty: int = 10,
):
    """Return a new target_function that uses the specified verifier."""

    def target_function(
        config: Configuration, instance: str, seed: int = 1
    ) -> float:
        # TODO: Parse network and property
        verifier_instance = verifier()

        before_t = time.perf_counter()
        result = verifier_instance.verify_property(
            Path(), Path(), config=config
        )
        took_t = time.perf_counter() - before_t

        # If the result is an err, we raise an exception. SMAC automatically
        # sets the cost to infinite if an exception is raised in the target_func
        verification_result = result.unwrap_or_raise(Exception)

        if verification_result.result == "TIMEOUT":
            took_t *= timeout_penalty

        return took_t

    return target_function
