from typing import Callable

from .dummy_verifier import install as install_dummy_verifier

installers: dict[str, Callable[[], None]] = {
    "DummyVerifier": install_dummy_verifier,
}


__all__ = ["installers"]
