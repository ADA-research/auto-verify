from pathlib import Path

from autoverify.verifier import Nnenum
from scripts.baselines.mnist.baseline import run_mnist_baseline

portfolio = [
    (Nnenum, None),  # nnenum + default config
]

run_mnist_baseline(portfolio, Path("TODO"))  # type: ignore
