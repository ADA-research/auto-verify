from pathlib import Path

from autoverify.portfolio.run.sequential_runner import run_sequential_portfolio
from autoverify.util.env import get_file_path
from autoverify.util.instances import read_vnncomp_instances
from autoverify.verifier.complete import OvalBab

if __name__ == "__main__":
    mnist_instances = read_vnncomp_instances("mnist_fc")
    file_path = get_file_path(Path(__file__))

    portfolio = [
        (OvalBab, file_path / "mnist_small.yaml"),
        (OvalBab, file_path / "mnist.yaml"),
    ]

    run_sequential_portfolio(
        portfolio,  # type: ignore
        mnist_instances,
        output_csv_path=Path("./abcrown_mnist_out.csv"),
    )
