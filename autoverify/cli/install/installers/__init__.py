from pathlib import Path
from typing import Callable

from .dummy.install import install as install_dummy_verifier
from .nnenum.install import install as install_nnenum

installers: dict[str, Callable[[Path], None]] = {
    "DummyVerifier": install_dummy_verifier,
    "nnenum": install_nnenum,
}

__all__ = ["installers"]
