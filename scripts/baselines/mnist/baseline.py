from pathlib import Path

from autoverify.portfolio.portfolio import Portfolio
from autoverify.portfolio.run.sequential_runner import run_sequential_portfolio
from autoverify.util.instances import (
    VerificationDataResult,
    read_vnncomp_instances,
)
from autoverify.util.loggers import experiment_logger

mnist_instances = read_vnncomp_instances("mnist_fc")


def run_mnist_baseline(
    portfolio: Portfolio,
    output_csv: Path,
) -> list[VerificationDataResult]:
    # Run once and discard
    experiment_logger.info("Init run")
    run_sequential_portfolio(
        portfolio[0:1],  # type: ignore
        mnist_instances[0:1],
        output_csv_path=output_csv,
    )

    experiment_logger.info("Real run")
    results = run_sequential_portfolio(
        portfolio,  # type: ignore
        mnist_instances,
        output_csv_path=output_csv,
    )

    return results
