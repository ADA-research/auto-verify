from pathlib import Path
from typing import Callable

from .dummy_verifier import install as install_dummy_verifier
from .nnenum import install as install_nnenum

installers: dict[str, Callable[[Path], None]] = {
    "DummyVerifier": install_dummy_verifier,
    "nnenum": install_nnenum,
}


__all__ = ["installers"]
