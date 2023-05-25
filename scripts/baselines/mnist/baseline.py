from pathlib import Path

from autoverify.portfolio.portfolio import Portfolio
from autoverify.portfolio.run.sequential_runner import run_sequential_portfolio
from autoverify.util.instances import (
    VerificationDataResult,
    read_vnncomp_instances,
)

mnist_instances = read_vnncomp_instances("mnist_fc")


def run_mnist_baseline(
    portfolio: Portfolio,
    output_csv: Path,
) -> list[VerificationDataResult]:
    # Run once and discard
    #
    # print("Init Run")
    # run_sequential_portfolio(
    #     portfolio,  # type: ignore
    #     mnist_instances[0:1],
    #     output_csv_path=output_csv,
    # )

    mnist_instances2 = [
        i
        for i in mnist_instances
        if i.property.name == "prop_8_0.03.vnnlib"
        and i.network.name == "mnist-net_256x4.onnx"
    ]
    print(len(mnist_instances2))

    print("Real run")
    results = run_sequential_portfolio(
        portfolio,  # type: ignore
        mnist_instances2,
        output_csv_path=output_csv,
    )

    return results
