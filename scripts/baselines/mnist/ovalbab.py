from pathlib import Path

from autoverify.util.env import get_file_path
from autoverify.verifier import OvalBab
from scripts.baselines.mnist.baseline import run_mnist_baseline

config_files = get_file_path(Path(__file__)) / "config_files"

portfolio = [
    (OvalBab, config_files / "ovalbab_mnist.json"),
]

run_mnist_baseline(portfolio, Path("TODO.csv"))  # type: ignore
