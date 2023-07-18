"""_summary_."""
from pathlib import Path
from typing import Callable, Type

from ConfigSpace import Configuration

from autoverify.util.instances import VerificationInstance
from autoverify.util.verifiers import verifier_from_name
from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier

# target_function(config, instance, seed) -> cost
SmacTargetFunction = Callable[[Configuration, str, int], float]


def _process_target_function_result(
    result: CompleteVerificationResult,
    timeout_penalty: int,
) -> float:
    """Process the verification result, TODO.

    Args:
        result: TODO.
        timeout_penalty: TODO.

    Returns:
        float: TODO.
    """
    # If the result is an err, we raise an exception. SMAC automatically
    # sets the cost to infinite if an exception is raised in the target_function
    verification_result = result.unwrap_or_raise(Exception)

    if verification_result.result == "TIMEOUT":
        verification_result.took *= timeout_penalty

    return float(verification_result.took)


def run_verification_instance(
    verifier: type[CompleteVerifier],
    config: Configuration | Path | None,
    instance: str | VerificationInstance,
    *,
    batch_size: int | None = None,
) -> CompleteVerificationResult:
    """Run an instance and report the result and time taken.

    Args:
        verifier: TODO.
        config: TODO.
        instance: TODO.

    Returns:
        tuple[CompleteVerificationResult, float]: TODO.
    """
    verifier_instance = verifier()

    if isinstance(instance, VerificationInstance):
        instance = instance.as_smac_instance()

    network, property, timeout = instance.split(",")

    result = verifier_instance.verify_property(
        Path(network),
        Path(property),
        config=config,
        timeout=int(timeout),
        batch_size=batch_size,
    )

    return result


def make_verifier_target_function(
    verifier: type[CompleteVerifier],
    *,
    timeout_penalty: int = 10,
    batch_size: int | None = None,
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
        result = run_verification_instance(
            verifier, config, instance, batch_size=batch_size
        )

        return _process_target_function_result(result, timeout_penalty)

    return target_function


def make_pick_verifier_target_function(
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
        # config["seed"] = seed
        verifier = verifier_from_name(config["verifier"])

        # FIXME: Verifier type mismatch between CompleteVerifier and Verifier
        result = run_verification_instance(
            verifier,  # type: ignore
            None,
            instance,
        )

        return _process_target_function_result(result, timeout_penalty)

    return target_function
