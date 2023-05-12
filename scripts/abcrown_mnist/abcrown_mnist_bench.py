from pathlib import Path

from autoverify.portfolio.run.sequential_runner import run_sequential_portfolio
from autoverify.util.env import get_file_path
from autoverify.util.instances import (
    VerificationInstance,
    read_vnncomp_instances,
)
from autoverify.verifier.complete import AbCrown


def filter_to_small(
    mnist_instances: list[VerificationInstance],
) -> list[str]:
    small_instances = []

    for inst in mnist_instances:
        size = inst.network.name.split(".")[0][-1]

        if size == "2":
            small_instances.append(inst.as_smac_instance())

    return small_instances


def mnist_features(
    mnist_instances: list[VerificationInstance],
) -> dict[str, list[float]]:
    features = {}

    for inst in mnist_instances:
        size = inst.network.name.split(".")[0][-1]
        features[inst] = [size]

    return features


if __name__ == "__main__":
    mnist_instances = read_vnncomp_instances("mnist_fc")
    file_path = get_file_path(Path(__file__))

    portfolio = [
        (AbCrown, file_path / "mnist_small.yaml"),
        (AbCrown, file_path / "mnist.yaml"),
    ]

    run_sequential_portfolio(
        portfolio,  # type: ignore
        mnist_instances,
        output_csv_path=Path("./abcrown_mnist_out.csv"),
    )
