"""_summary_."""
from pathlib import Path

from ConfigSpace import Configuration

from autoverify.types import Cost, Instance, Seed, TargetFunction
from autoverify.util.verification_instance import VerificationInstance
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp import inst_bench_to_kwargs, inst_bench_to_verifier
from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier, Verifier

# Penalized Average Runtime
# If an instance times out, its cost becomes cost * PAR
_DEFAULT_PAR = 10


def _run_verification_instance(
    verifier: CompleteVerifier,
    config: Configuration | Path | None,
    instance: Instance | VerificationInstance,
) -> CompleteVerificationResult:
    """Run an instance and report the result and time taken.

    Args:
        verifier: CompleteVerifier to run.
        config: Config to use during verification.
        instance: Instance to run.

    Returns:
        CompleteVerificationResult: Outcome of the verification.
    """
    if isinstance(instance, VerificationInstance):
        instance = instance.as_smac_instance()

    # FIXME: What if there are commas in the net or prop name?
    # This problem occurs in multiple parts where we work with SMAC instances
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
        result: Result of the veriication.
        timeout_penalty: PAR score.

    Returns:
        float: Walltime cost.
    """
    # If the result is an err, we raise an exception. SMAC automatically
    # sets the cost to infinite if an exception is raised in the target_function
    verification_result = result.unwrap_or_raise(Exception)

    if verification_result.result == "TIMEOUT":
        verification_result.took *= timeout_penalty

    return float(verification_result.took)


def get_vnn_verifier_tf(
    verifier: str,
    benchmark: str,
    *,
    timeout_penalty: int = _DEFAULT_PAR,
) -> TargetFunction:
    """Get a tf for a vnncomp benchmark from a name."""

    def target_function(
        config: Configuration, instance: Instance, seed: Seed
    ) -> Cost:
        """_summary_."""
        seed += 1  # silence warning, cant rename the param to _ or smac errors

        verifier_inst = inst_bench_to_verifier(
            benchmark, VerificationInstance.from_str(instance), verifier
        )

        result = _run_verification_instance(verifier_inst, config, instance)
        return _process_target_function_result(result, timeout_penalty)

    return target_function


def get_verifier_tf(
    verifier: Verifier, *, timeout_penalty: int = _DEFAULT_PAR
) -> TargetFunction:
    """Get a target function to use in SMAC for a verifier."""

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
