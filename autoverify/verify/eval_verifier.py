"""Evaluate the performance of a verifier on a set of instances.

This file is meant for functions that benchmark the performance of a verifier,
collecting detailed results about the verification run.
"""
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
from autoverify.verifier.verifier import CompleteVerifier

logger = logging.getLogger(__name__)


def eval_verifier(
    verifier: CompleteVerifier,
    instances: list[VerificationInstance],
    config: Configuration | Path | None,
    *,
    warmup: bool = True,
    output_csv_path: Path | None = None,
) -> list[VerificationDataResult]:
    """_summary_."""
    if output_csv_path is not None:
        init_verification_result_csv(output_csv_path)

    if warmup:
        logger.info("Starting warmup run")
        verifier.verify_instance(instances[0], config=config)
        logger.info("Finished warmup run")

    results: list[VerificationDataResult] = []

    for i, instance in enumerate(instances):
        logger.info(
            f"\nVerifying instance {i}; property {instance.property.name} on "
            f"{instance.network.name} with verifier {verifier.name} and "
            f"configuration {config or 'default'} "
            f"(timeout = {instance.timeout} sec.)"
        )

        verification_data: VerificationDataResult | None = None
        result = verifier.verify_instance(instance, config=config)

        if isinstance(result, Ok):
            logger.info("Verification finished succesfully.")
            result = result.unwrap()
            logger.info(f"Result: {result.result}")

            verification_data = VerificationDataResult(
                instance.network.name,
                instance.property.name,
                instance.timeout,
                verifier.name,
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
                verifier.name,
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
