import sys
from pathlib import Path

from ConfigSpace import Configuration

from autoverify.verifier import Nnenum
from autoverify.verifier.complete.nnenum.nnenum_configspace import (
    NnenumConfigspace,
)
from scripts.baselines.mnist.baseline import run_mnist_baseline

# the `auto` option just picks between control and image based on instance
cfg_control = Configuration(NnenumConfigspace, {"settings_mode": "control"})
cfg_image = Configuration(NnenumConfigspace, {"settings_mode": "image"})
cfg_exact = Configuration(NnenumConfigspace, {"settings_mode": "exact"})

portfolio = [
    (Nnenum, cfg_control),
    (Nnenum, cfg_image),
    (Nnenum, cfg_exact),
]

if __name__ == "__main__":
    run_mnist_baseline(portfolio, Path(sys.argv[1]))  # type: ignore
