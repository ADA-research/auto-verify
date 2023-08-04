from pathlib import Path

from ConfigSpace import Configuration

from autoverify.types import Cost, Instance, Seed, TargetFunction
from autoverify.util.instances import VerificationInstance
from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier, Verifier


def _run_verification_instance(
    verifier: CompleteVerifier,
    config: Configuration | Path | None,
    instance: Instance | VerificationInstance,
) -> CompleteVerificationResult:
    """Run an instance and report the result and time taken.

    Args:
        verifier: TODO.
        config: TODO.
        instance: TODO.

    Returns:
        tuple[CompleteVerificationResult, float]: TODO.
    """
    if isinstance(instance, VerificationInstance):
        instance = instance.as_smac_instance()

    # FIXME: What if there are commas in the net or prop name?
    network, property, timeout = instance.split(",")

    result = verifier.verify_property(
        Path(network),
        Path(property),
        config=config,
        timeout=int(timeout),
    )

    return result


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


def get_verifier_tf(
    verifier: Verifier, *, timeout_penalty: int = 10
) -> TargetFunction:
    """_summary_."""

    def target_function(
        config: Configuration, instance: Instance, seed: Seed
    ) -> Cost:
        """_summary_."""
        seed += 1  # silence warning, cant rename the param to _ or smac errors

        # NOTE: `Verifier` doesn't implement `verify_property`
        # So why arent we saying verifier: CompleteVerifier
        assert isinstance(verifier, CompleteVerifier)

        result = _run_verification_instance(verifier, config, instance)
        return _process_target_function_result(result, timeout_penalty)

    return target_function


def get_pick_tf(
    verifiers: list[Verifier], *, timeout_penalty: int = 10
) -> TargetFunction:
    """_summary_."""

    def target_function(
        config: Configuration, instance: Instance, seed: Seed
    ) -> Cost:
        """_summary_."""
        seed += 1  # silence warning, cant rename the param to _ or smac errors
        result = _run_verification_instance(
            verifiers[config["index"]],
            None,
            instance,
        )

        return _process_target_function_result(result, timeout_penalty)

    return target_function