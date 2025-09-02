from collections.abc import Callable
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo

from .abcrown.install import AbCrownRepoInfo
from .abcrown.install import install as install_abcrown
from .mnbab.install import MnBabRepoInfo
from .mnbab.install import install as install_mnbab
from .nnenum.install import NnenumRepoInfo
from .nnenum.install import install as install_nnenum
from .ovalbab.install import OvalBabRepoInfo
from .ovalbab.install import install as install_ovalbab
from .verinet.install import VerinetRepoInfo
from .verinet.install import install as install_verinet

installers: dict[str, Callable[[Path], None]] = {
    "nnenum": install_nnenum,
    "abcrown": install_abcrown,
    "mnbab": install_mnbab,
    "ovalbab": install_ovalbab,
    "verinet": install_verinet,
}

repo_infos: dict[str, GitRepoInfo] = {
    "nnenum": NnenumRepoInfo,
    "abcrown": AbCrownRepoInfo,
    "mnbab": MnBabRepoInfo,
    "ovalbab": OvalBabRepoInfo,
    "verinet": VerinetRepoInfo,
}

__all__ = [
    "installers",
    "repo_infos",
]
