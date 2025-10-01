"""ovalbab installer."""

import os
import subprocess
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import (
    create_env_from_file,
    get_conda_path,
    get_conda_source_cmd,
)
from autoverify.util.env import copy_env_file_to

OvalBabRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="5de3113",
    clone_url="https://github.com/oval-group/oval-bab",
)


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs ovalbab.

    Args:
        install_dir: Path where oval-bab is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository with version management
    clone_checkout_verifier(OvalBabRepoInfo, install_dir, custom_commit=custom_commit, use_latest=use_latest)

    # Copy environment file and create conda environment
    copy_env_file_to(Path(__file__), install_dir)
    print("Creating conda environment...")
    create_env_from_file(install_dir / "environment.yml")

    os.chdir(install_dir / "tool")

    source_cmd = get_conda_source_cmd(get_conda_path())
    print("Installing ovalbab package...")
    install_cmd = f"""
    {" ".join(source_cmd)}
    conda activate __av__ovalbab
    pip install .
    """

    subprocess.run(install_cmd, executable="/bin/bash", shell=True, check=True)

    # Print installation information
    print("\nOVALBAB (conda) Installation Complete")
    print(f"Installation directory: {install_dir}")
    print("To activate: conda activate __av__ovalbab")
