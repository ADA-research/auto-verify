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

    for instance in instances:
        logger.info(
            f"Verifying property {instance.property.name} on "
            f"{instance.network.name} with verifier {verifier.name} and "
            f"configuration {config or 'default'}, "
            f"(timeout = {instance.timeout} sec.)"
        )

        verification_data: VerificationDataResult | None = None
        result = verifier.verify_instance(instance, config=config)

        if isinstance(result, Ok):
            logger.info("Verification finished succesfully.")
            logger.info(f"Result: {result.value.result}")

            verification_data = VerificationDataResult(
                instance.network.name,
                instance.property.name,
                instance.timeout,
                verifier.name,
                str(config),
                "OK",
                result.value.result,
                result.value.took,
                result.value.counter_example,
                None,
            )
            results.append(verification_data)
        elif isinstance(result, Err):
            err_string = result.unwrap_err().err

            logger.info("Exception during verification.")
            logger.info(err_string)

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
                else DEFAULT_VERIFICATION_TIMEOUT_SEC,  # TODO: This is bad
                None,
                err_string,
            )

        logger.info(f"Verification took {result.value.took} seconds.")

        if output_csv_path is not None and isinstance(
            verification_data, VerificationDataResult
        ):
            csv_append_verification_result(verification_data, output_csv_path)

    return results
