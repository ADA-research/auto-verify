from pathlib import Path

from autoverify.util.env import get_file_path
from autoverify.verifier import AbCrown
from autoverify.verifier.complete.nnenum.nnenum_verifier import Nnenum
from scripts.baselines.mnist.baseline import run_mnist_baseline

config_files = get_file_path(Path(__file__)) / "config_files"

portfolio = [
    (AbCrown, config_files / "abcrown_mnist_small.yaml"),
    (AbCrown, config_files / "abcrown_mnist.yaml"),
]

run_mnist_baseline(portfolio, Path("TODO.csv"))  # type: ignore
