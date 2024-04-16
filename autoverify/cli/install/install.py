"""TODO summary."""

import logging
import shlex
import shutil
import subprocess
from collections.abc import Iterable
from subprocess import CalledProcessError

from result import Err, Ok, Result
from xdg_base_dirs import xdg_data_home

from autoverify.util.conda import (
    delete_conda_env,
    get_av_conda_envs,
    get_verifier_conda_env_name,
)
from autoverify.util.env import cwd

from .installers import installers, repo_infos

AV_HOME = xdg_data_home() / "autoverify"
VERIFIER_DIR = AV_HOME / "verifiers"
TOOL_DIR_NAME = "tool"


def _create_base_dirs():
    """Creates the $XDG_DATA_HOME/autoverify/verifiers directories."""
    VERIFIER_DIR.mkdir(parents=True, exist_ok=True)


def _remove_verifier_dir(verifier: str):
    """Removes the directory associated with the verifier."""
    print(f"Removing {verifier} directory")
    shutil.rmtree(VERIFIER_DIR / verifier)


def _init_new_verifier_dir(dir_name: str):
    """Creates a new directory in `VERIFIER_DIR` with specified name."""
    dir_path = VERIFIER_DIR / dir_name
    dir_path.mkdir()


def _uninstall_verifier(verifier: str) -> Result[None, str]:
    """Tries to uninstall the specified verifier."""
    try:
        _remove_verifier_dir(verifier)
    except Exception as err:
        print(f"Error removing verifier directory: {err=}")
        return Err("Exception when deleting verifier directory")

    conda_env_name = get_verifier_conda_env_name(verifier)

    if conda_env_name and conda_env_name in get_av_conda_envs():
        try:
            delete_conda_env(conda_env_name)
        except Exception as err:
            print(f"Error deleting conda env: {err=}")
            return Err("Exception when deleting conda env")

    return Ok()


def _install_verifier(verifier: str) -> Result[None, str]:
    """Tries to install the specified verifier."""
    if verifier not in installers:
        return Err(f"No installer found for verifier {verifier}")

    try:
        _init_new_verifier_dir(verifier)
    except Exception as err:
        print(f"Error initializing new verifier directory: {err=}")
        return Err("Directory initialization failed")

    dir_path = VERIFIER_DIR / verifier

    try:
        installers[verifier](dir_path)
        return Ok()
    except Exception as err:
        if isinstance(err, CalledProcessError):
            err = err.stderr.decode("utf-8")

        logging.exception(err)
        _remove_verifier_dir(verifier)
        return Err("Exception during installation")


def try_install_verifiers(verifiers: Iterable[str]):
    """Tries to install the specified verifiers.

    Will print the result of each attempt to stdout.

    Args:
        verifiers: Names of the verifiers to install.
    """
    _create_base_dirs()

    for verifier in verifiers:
        print(f"\nInstalling {verifier}...")

        install_result = _install_verifier(verifier)

        if isinstance(install_result, Ok):
            print(f"Succesfully installed {verifier}")
        elif isinstance(install_result, Err):
            print(f"Error installing {verifier}: {install_result.err()}")


def try_uninstall_verifiers(verifiers: Iterable[str]):
    """Tries to uninstall the specified verifiers.

    Will print the result of each attempt to stdout.

    Args:
        verifiers: Names of the verifiers to uninstall.
    """
    for verifier in verifiers:
        print(f"\nUninstalling {verifier}...")

        uninstall_result = _uninstall_verifier(verifier)

        if isinstance(uninstall_result, Ok):
            print(f"Succesfully uninstalled {verifier}")
        elif isinstance(uninstall_result, Err):
            print(f"Error uninstalling {verifier}: {uninstall_result.err()}")


def check_commit_hashes():
    """Check if all commit hashes are up to date."""
    all_up_to_date = True

    for file in VERIFIER_DIR.iterdir():
        if not file.is_dir():
            continue

        repo_info = repo_infos[file.name]
        cmd = f"git rev-parse {repo_info.branch}"

        with cwd(file / "tool"):
            commit_hash = subprocess.run(
                shlex.split(cmd), capture_output=True
            ).stdout.decode()

            # Currently have short hashes in install files
            # Switching to long ones might be good
            commit_hash = commit_hash[:7]

            if commit_hash != repo_info.commit_hash:
                all_up_to_date = False
                print(
                    f"Verifier {file.name} has commit_hash {commit_hash}, "
                    f"but commit hash in installation file "
                    f"is {repo_info.commit_hash}"
                )

    if all_up_to_date:
        print("Everything up to date.")
