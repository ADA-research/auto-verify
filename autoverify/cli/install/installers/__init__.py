from pathlib import Path
from typing import Callable

from .abcrown.install import install as install_abcrown
from .dummy.install import install as install_dummy_verifier
from .mnbab.install import install as install_mnbab
from .nnenum.install import install as install_nnenum

installers: dict[str, Callable[[Path], None]] = {
    "DummyVerifier": install_dummy_verifier,
    "nnenum": install_nnenum,
    "abcrown": install_abcrown,
    "mnbab": install_mnbab,
}

__all__ = ["installers"]
