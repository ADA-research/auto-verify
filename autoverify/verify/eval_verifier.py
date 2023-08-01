"""Evaluate the performance of a verifier on a set of instances.

This file is meant for functions that benchmark the performance of a verifier,
collecting detailed results about the verification run.
"""
import copy
import logging
from pathlib import Path

from ConfigSpace import Configuration
from result import Err, Ok

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util.instances import (
    VerificationDataResult,
    VerificationInstance,
    csv_append_verification_result,
    init_verification_result_csv,
)
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp import inst_bench_to_verifier
from autoverify.verifier.verifier import CompleteVerifier

logger = logging.getLogger(__name__)


def _warmup(
    verifier: CompleteVerifier | str,
    instance: VerificationInstance,
    config: Configuration | Path | None,
):
    logger.info("Starting warmup run")
    warmup_inst = copy.deepcopy(instance)
    warmup_inst.timeout = 10

    if isinstance(verifier, str):
        v = verifier_from_name(verifier)()
        assert isinstance(v, CompleteVerifier)
        v.verify_instance(warmup_inst, config=config)
    else:
        verifier.verify_instance(warmup_inst, config=config)

    logger.info("Finished warmup run")


def eval_verifier(
    verifier: CompleteVerifier | str,
    instances: list[VerificationInstance],
    config: Configuration | Path | None,
    *,
    warmup: bool = True,
    output_csv_path: Path | None = None,
    fetch_vnnc_verifier: bool = False,
    benchmark_name: str | None = None,
) -> list[VerificationDataResult]:
    """_summary_."""
    if isinstance(verifier, str):
        assert (
            fetch_vnnc_verifier is True
        ), "verifier str type only used for VNNCOMP eval"
        assert (
            benchmark_name is not None
        ), "Need a benchmark name if verifier is str"

    if output_csv_path is not None:
        init_verification_result_csv(output_csv_path)

    if warmup:
        _warmup(verifier, instances[0], config)

    results: list[VerificationDataResult] = []

    for i, instance in enumerate(instances):
        iter_verifier: CompleteVerifier
        if isinstance(verifier, str):
            assert benchmark_name is not None
            iter_verifier = inst_bench_to_verifier(
                benchmark_name, instance, verifier
            )
        else:
            iter_verifier = verifier

        logger.info(
            f"\nVerifying instance {i}; property {instance.property.name} on "
            f"{instance.network.name} with verifier {iter_verifier.name} and "
            f"configuration {config or 'default'} "
            f"(timeout = {instance.timeout} sec.)"
        )

        verification_data: VerificationDataResult | None = None
        result = iter_verifier.verify_instance(instance, config=config)

        if isinstance(result, Ok):
            logger.info("Verification finished succesfully.")
            result = result.unwrap()
            logger.info(f"Result: {result.result}")

            verification_data = VerificationDataResult(
                instance.network.name,
                instance.property.name,
                instance.timeout,
                iter_verifier.name,
                str(config),
                "OK",
                result.result,
                result.took,
                result.counter_example,
                result.err,
                result.stdout,
            )
            results.append(verification_data)
        elif isinstance(result, Err):
            result = result.unwrap_err()

            logger.info("Exception during verification.")
            logger.info(result.err)

            verification_data = VerificationDataResult(
                instance.network.name,
                instance.property.name,
                instance.timeout,
                iter_verifier.name,
                str(config),
                "ERR",
                "ERR",
                float(instance.timeout)
                if instance.timeout
                else DEFAULT_VERIFICATION_TIMEOUT_SEC,
                None,
                result.err,
                result.stdout,
            )
            results.append(verification_data)

        logger.info(f"Verification took {result.took} seconds.")

        if output_csv_path is not None and isinstance(
            verification_data, VerificationDataResult
        ):
            csv_append_verification_result(verification_data, output_csv_path)

    return results
