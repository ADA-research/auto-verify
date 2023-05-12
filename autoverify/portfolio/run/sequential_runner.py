"""_summary_."""
from pathlib import Path
from typing import Type

import pandas as pd
from ConfigSpace import Configuration
from result import Err, Ok

from autoverify.portfolio.target_function import run_verification_instance
from autoverify.util.instances import (
    VerificationDataResult,
    VerificationInstance,
    append_verification_result_to_csv,
)
from autoverify.util.loggers import verification_logger
from autoverify.verifier.verifier import CompleteVerifier


def append_df(
    df: pd.DataFrame, verification_data: VerificationDataResult
) -> pd.DataFrame:
    """Append the dataclass to the dataframe."""
    return pd.concat([df, pd.DataFrame([verification_data])])


def run_sequential_portfolio(
    portfolio: list[tuple[Type[CompleteVerifier], Configuration | Path]],
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
                f"{instance.network.name} with verifier {verifier.name} and "
                f"configuration {config}"
            )

            result, took_t = run_verification_instance(
                verifier, config, instance.as_smac_instance()
            )

            verification_data: VerificationDataResult | None = None

            if isinstance(result, Ok):
                verification_logger.info("Verification finished succesfully.")
                verification_logger.info(f"Result: {result.value.result}")

                verification_data = VerificationDataResult(
                    instance.network.name,
                    instance.property.name,
                    verifier().name,
                    str(config),
                    "OK",
                    result.value.result,
                    took_t,
                    result.value.counter_example,
                    None,
                )
                results.append(verification_data)
            elif isinstance(result, Err):
                verification_logger.info("Exception during verification.")
                verification_logger.info(result.unwrap_err())

                verification_data = VerificationDataResult(
                    instance.network.name,
                    instance.property.name,
                    verifier().name,
                    str(config),
                    "ERR",
                    None,
                    took_t,
                    None,
                    result.unwrap_err(),
                )
                results.append(verification_data)

            verification_logger.info(f"Verification took {took_t} seconds.")

            if output_csv_path is None:
                continue

            if isinstance(verification_data, VerificationDataResult):
                append_verification_result_to_csv(
                    verification_data, output_csv_path
                )

    return results
