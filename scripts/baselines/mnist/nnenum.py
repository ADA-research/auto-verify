from pathlib import Path

from ConfigSpace import Configuration

from autoverify.verifier import Nnenum
from autoverify.verifier.complete.nnenum.nnenum_configspace import (
    NnenumConfigspace,
)
from scripts.baselines.mnist.baseline import run_mnist_baseline

cfg_control = Configuration(NnenumConfigspace, {"settings_mode": "control"})
cfg_image = Configuration(NnenumConfigspace, {"settings_mode": "image"})
cfg_exact = Configuration(NnenumConfigspace, {"settings_mode": "exact"})

portfolio = [
    (Nnenum, cfg_control),
    (Nnenum, cfg_image),
    (Nnenum, cfg_exact),
]


run_mnist_baseline(portfolio, Path("TODO"))  # type: ignore
