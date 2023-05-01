"""nnenum installer."""
import os
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
from autoverify.util.env import copy_env_file_to, environment

MnBabRepoInfo = GitRepoInfo(
    MAIN_BRANCH="main",
    COMMIT_HASH="6aa5272",
    CLONE_URL="https://github.com/eth-sri/mn-bab",
)


def install(install_dir: Path):
    """_summary_."""
    clone_checkout_verifier(MnBabRepoInfo, install_dir)
    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "environment.yml")

    os.chdir(install_dir / "tool")

    source_cmd = get_conda_source_cmd(get_conda_path())
    # HACK: This is bad, should upload ELINA as a conda package
    # Also have to comment out line with cddlib_prefix else the CDDLIB_PREFIX
    # doesnt work? Also need a way to get around that `sudo`
    elina_cmd = f"""
    {" ".join(source_cmd)}
    conda activate __av__mnbab
    git clone https://github.com/eth-sri/ELINA.git
    cd ELINA
    sed -i '58 s/^/#/' configure
    ./configure -use-deeppoly -use-fconv
    make
    sudo make install
    cd ..
    """

    # TODO: Parse versions and build from the environment.yml file
    mpfr_path = str(get_conda_pkg_path("mpfr", "4.0.2", "hb69a4c5_1"))
    cddlib_path = str(get_conda_pkg_path("cddlib", "1!0.94j", "he80fd80_1001"))

    with environment(MPFR_PREFIX=mpfr_path, CDD_PREFIX=cddlib_path):
        subprocess.run(
            elina_cmd,
            executable="/bin/bash",
            shell=True,
        )
