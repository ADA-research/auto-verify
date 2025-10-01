"""Mnbab installer."""

import shlex
import subprocess
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import (
    create_env_from_file,
    get_conda_path,
    get_conda_pkg_path,
    get_conda_source_cmd,
)
from autoverify.util.env import copy_env_file_to, cwd, environment

MnBabRepoInfo = GitRepoInfo(
    branch="SABR_ready",
    commit_hash="70751b8",
    clone_url="https://github.com/eth-sri/mn-bab",
)


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs mnbab.

    Args:
        install_dir: Path where mn-bab is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository with version management
    clone_checkout_verifier(
        MnBabRepoInfo, install_dir, init_submodules=True, custom_commit=custom_commit, use_latest=use_latest
    )

    # Copy environment file and create conda environment
    copy_env_file_to(Path(__file__), install_dir)
    print("Creating conda environment...")
    create_env_from_file(install_dir / "environment.yml")

    with cwd(install_dir):
        subprocess.run(shlex.split("mkdir deps"), check=True)

    source_cmd = get_conda_source_cmd(get_conda_path())

    # HACK: This is bad, should upload ELINA as a conda package
    # Also have to comment out line with cdd_prefix else the CDD_PREFIX
    # doesnt work?
    print("Building ELINA dependencies...")
    elina_cmd = f"""
    {" ".join(source_cmd)}
    conda activate __av__mnbab
    git clone https://github.com/eth-sri/ELINA.git
    cd ELINA
    sed -i '58 s/^/#/' configure
    ./configure -use-deeppoly -use-fconv --prefix {str(install_dir / "deps")}
    make
    make install
    cd ..
    export PYTHONPATH=$PYTHONPATH:$PWD
    """

    # TODO: Parse versions and build from the environment.yml file
    mpfr_path = str(get_conda_pkg_path("mpfr", "4.0.2", "hb69a4c5_1"))
    cddlib_path = str(get_conda_pkg_path("cddlib", "1!0.94j", "he80fd80_1001"))

    with (
        cwd(install_dir / "tool"),
        environment(MPFR_PREFIX=mpfr_path, CDD_PREFIX=cddlib_path),
    ):
        subprocess.run(elina_cmd, shell=True)

    # Print installation information
    print("\nMNBAB (conda) Installation Complete")
    print(f"Installation directory: {install_dir}")
    print("To activate: conda activate __av__mnbab")
    print("Note: ELINA has been compiled and installed in the deps directory")
