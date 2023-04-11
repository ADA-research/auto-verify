from pathlib import Path
from typing import Callable

from .dummy_verifier import install as install_dummy_verifier

installers: dict[str, Callable[[Path], None]] = {
    "DummyVerifier": install_dummy_verifier,
}


__all__ = ["installers"]
