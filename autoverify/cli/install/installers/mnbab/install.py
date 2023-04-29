"""nnenum installer."""
import os
import shlex
import subprocess
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

MnBabRepoInfo = GitRepoInfo(
    MAIN_BRANCH="main",
    COMMIT_HASH="6aa5272",
    CLONE_URL="https://github.com/eth-sri/mn-bab",
)


# ELINA setup
#
# Go into top level directory of repo:
#
# cd mn-bab
#
# Setup ELINA:
#
# git clone https://github.com/eth-sri/ELINA.git
# cd ELINA
# ./configure -use-deeppoly -use-fconv
# make
# sudo make install
# cd ..
#
# https://github.com/eth-sri/mn-bab/blob/SABR_ready/configs/vnncomp22/default_config.json
#
# TODO: Make the env file, most deps are on anaconda
def install(install_dir: Path):
    """_summary_."""
    clone_checkout_verifier(MnBabRepoInfo, install_dir)
    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "environment.yml")

    # TODO: Export mpfr path
    # TODO: Cddlib path doesnt work unless u modify configure??
    # TODO: Make this command below work

    elina_install_cmd = """git clone https://github.com/eth-sri/ELINA.git && \
    cd ELINA && \
    ./configure -use-deeppoly -use-fconv && \
    make && \
    sudo make install && \
    cd ..
    """

    os.chdir(install_dir / "tool")

    # TODO: Upload ELINA as conda package?
    subprocess.run(shlex.split(elina_install_cmd), shell=True)
