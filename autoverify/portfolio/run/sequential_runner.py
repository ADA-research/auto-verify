"""_summary_."""
from pathlib import Path
from typing import Type

from ConfigSpace import Configuration
from result import Err, Ok

from autoverify.portfolio.target_function import run_verification_instance
from autoverify.util.instances import (
    VerificationDataResult,
    VerificationInstance,
    write_verification_data_results_to_csv,
)
from autoverify.util.loggers import verification_logger
from autoverify.verifier.verifier import CompleteVerifier


def run_sequential_portfolio(
    portfolio: list[tuple[Type[CompleteVerifier], Configuration]],
    instances: list[VerificationInstance],
    *,
    output_csv_path: Path | None = None,
) -> list[VerificationDataResult]:
    """Run a portfolio sequentially on a set of instances.

    This is a very naive function meant for quick experimenting, it will
    run a set of configurations on a set of instances one by one, meaning
    each config is ran on each instance, after which the results are accumulated
    and reported.

    Args:
        portfolio: TODO.
        instances: TODO.
        output_csv_path: TODO.

    Returns:
        list[VerificationDataResult]: TODO.
    """
    results: list[VerificationDataResult] = []

    for verifier, config in portfolio:
        for instance in instances:
            verification_logger.info(
                f"Verifying property {instance.property.name} on "
                f"{instance.network.name} with verifier {verifier.name}"
            )

            result, took_t = run_verification_instance(
                verifier, config, instance.as_smac_instance()
            )

            if isinstance(result, Ok):
                verification_logger.info("Verification finished succesfully.")
                verification_logger.info(f"Result: {result.value.result}")

                results.append(
                    VerificationDataResult(
                        instance.network.name,
                        instance.property.name,
                        "OK",
                        result.value.result,
                        result.value.counter_example,
                        None,
                    )
                )
            elif isinstance(result, Err):
                verification_logger.info("Exception during verification.")
                verification_logger.info(result.unwrap_err())
                results.append(
                    VerificationDataResult(
                        instance.network.name,
                        instance.property.name,
                        "OK",
                        None,
                        None,
                        result.unwrap_err(),
                    )
                )

            verification_logger.info(f"Verification took {took_t} seconds.")

    if output_csv_path is not None:
        write_verification_data_results_to_csv(results, output_csv_path)

    return results
