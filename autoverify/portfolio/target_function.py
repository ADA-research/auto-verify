"""_summary_."""
import time
from pathlib import Path
from typing import Callable, Type

from ConfigSpace import Configuration

from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier

# target_function(config, instance, seed) -> cost
SmacTargetFunction = Callable[[Configuration, str, int], float]


def run_verification_instance(
    verifier: Type[CompleteVerifier],
    config: Configuration | Path,
    instance: str,
) -> tuple[CompleteVerificationResult, float]:
    """Run an instance and report the result and time taken.

    Args:
        verifier: TODO.
        config: TODO.
        instance: TODO.

    Returns:
        tuple[CompleteVerificationResult, float]: TODO.
    """
    verifier_instance = verifier()
    network, property = instance.split(",")

    before_t = time.time()

    result = verifier_instance.verify_property(
        Path(network), Path(property), config=config
    )

    return result, time.time() - before_t


def make_verifier_target_function(
    verifier: Type[CompleteVerifier],
    *,
    timeout_penalty: int = 10,
) -> SmacTargetFunction:
    """Return a new target_function that uses the specified verifier.

    Args:
        verifier: The verifier class to use in the target function.
        timeout_penalty: The multiplier used for instances that have
            timed out, `cost *= timeout_penalty`.

    Returns:
        SmacTargetFunction: The target function that can be used inside
            a SMAC facade.
    """

    def target_function(
        config: Configuration, instance: str, seed: int = 1
    ) -> float:
        """Target function to be used inside the SMAC procedure.

        We do not actually care about the verification result here, we just
        report the `process_time` so SMAC can optimize for it.
        """
        seed += 1  # silence warning, cant rename the param to _ or smac errors
        result, took_t = run_verification_instance(verifier, config, instance)

        # If the result is an err, we raise an exception. SMAC automatically
        # sets the cost to infinite if an exception is raised in the target_func
        verification_result = result.unwrap_or_raise(Exception)

        if verification_result.result == "TIMEOUT":
            took_t *= timeout_penalty

        return took_t

    return target_function
