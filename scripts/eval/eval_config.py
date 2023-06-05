import sys
from pathlib import Path

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio
from autoverify.portfolio.run.sequential_runner import run_sequential_portfolio
from autoverify.util.configs import config_from_txt_file
from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.vnncomp_filters import mnist_small_filter
from autoverify.verifier import AbCrown

mnist_small = read_vnncomp_instances("mnist_fc", predicate=mnist_small_filter)
verifier = AbCrown


if __name__ == "__main__":
    config = config_from_txt_file(Path(sys.argv[1]), verifier.config_space)
    out_csv = Path(sys.argv[2])

    pf = Portfolio([ConfiguredVerifier(verifier.name, config)])

    mnist_small = mnist_small[:2]
    run_sequential_portfolio(
        pf,
        mnist_small,
        output_csv_path=out_csv,
        warmup=True,
    )
