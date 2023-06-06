import sys
from pathlib import Path

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio
from autoverify.portfolio.run.sequential_runner import run_sequential_portfolio
from autoverify.util.env import get_file_path
from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.vnncomp_filters import mnist_small_filter
from autoverify.verifier import AbCrown

mnist_small = read_vnncomp_instances("mnist_fc", predicate=mnist_small_filter)
verifier = AbCrown


if __name__ == "__main__":
    config = get_file_path(Path(__file__)) / "abcrown_mnist_small.yaml"
    out_csv = Path(sys.argv[1])

    pf = Portfolio([ConfiguredVerifier(verifier.name, config)])

    run_sequential_portfolio(
        pf, mnist_small, output_csv_path=out_csv, warmup=True
    )
