"""
Virtual environment based installers for auto-verify verifiers.

This module provides an alternative to conda-based installations using
Python virtual environments and uv for package management.
"""

from collections.abc import Callable
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo

from .abcrown.venv_install import VenvAbCrownRepoInfo
from .abcrown.venv_install import install as install_abcrown_venv
from .nnenum.venv_install import VenvNnenumRepoInfo
from .nnenum.venv_install import install as install_nnenum_venv
from .venv_install import (
    VENV_AV_HOME,
    VENV_VERIFIER_DIR,
    try_install_verifiers_venv,
    try_uninstall_verifiers_venv,
)
from .verinet.venv_install import VenvVerinetRepoInfo
from .verinet.venv_install import install as install_verinet_venv

venv_installers: dict[str, Callable[[Path], None]] = {
    "nnenum": install_nnenum_venv,
    "abcrown": install_abcrown_venv,
    "verinet": install_verinet_venv,
    # Add more verifiers as they get venv support
}

venv_repo_infos: dict[str, GitRepoInfo] = {
    "nnenum": VenvNnenumRepoInfo,
    "abcrown": VenvAbCrownRepoInfo,
    "verinet": VenvVerinetRepoInfo,
}

__all__ = [
    "VENV_AV_HOME",
    "VENV_VERIFIER_DIR", 
    "venv_installers",
    "venv_repo_infos",
    "try_install_verifiers_venv",
    "try_uninstall_verifiers_venv",
] 