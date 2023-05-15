"""_summary_."""
import time
from pathlib import Path
from typing import Callable, Type

from ConfigSpace import Configuration

from autoverify.util.verifiers import verifier_from_name
from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier

# target_function(config, instance, seed) -> cost
SmacTargetFunction = Callable[[Configuration, str, int], float]


def _process_target_function_result(
    result: CompleteVerificationResult,
    took_t: float,
    timeout_penalty: int,
) -> float:
    """Process the verification result, TODO.

    Args:
        result: TODO.
        took_t: TODO.
        timeout_penalty: TODO.

    Returns:
        float: TODO.
    """
    # If the result is an err, we raise an exception. SMAC automatically
    # sets the cost to infinite if an exception is raised in the target_func
    verification_result = result.unwrap_or_raise(Exception)

    if verification_result.result == "TIMEOUT":
        took_t *= timeout_penalty

    print("TOOK: ", took_t)

    return took_t


def run_verification_instance(
    verifier: Type[CompleteVerifier],
    config: Configuration | Path | None,
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

        return _process_target_function_result(result, took_t, timeout_penalty)

    return target_function


def make_select_verifier_target_function(
    *, timeout_penalty: int = 10
) -> SmacTargetFunction:
    """Return a new target_function for selecting a verifier.

    Args:
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
        verifier = verifier_from_name(config["verifier"])
        print(verifier)

        seed += 1  # silence warning, cant rename the param to _ or smac errors
        result, took_t = run_verification_instance(
            verifier,  # type: ignore FIXME: !!!
            None,
            instance,
        )

        return _process_target_function_result(result, took_t, timeout_penalty)

    return target_function
