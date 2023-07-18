from pathlib import Path
from typing import Callable

from .abcrown.install import install as install_abcrown
from .mnbab.install import install as install_mnbab
from .nnenum.install import install as install_nnenum
from .ovalbab.install import install as install_ovalbab
from .verinet.install import install as install_verinet

installers: dict[str, Callable[[Path], None]] = {
    "nnenum": install_nnenum,
    "abcrown": install_abcrown,
    "mnbab": install_mnbab,
    "ovalbab": install_ovalbab,
    "verinet": install_verinet,
}

__all__ = ["installers"]
