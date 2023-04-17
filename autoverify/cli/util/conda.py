"""Conda utility functions."""

import shlex
import subprocess
from pathlib import Path

AV_ENV_BASE_NAME = "__av__"


def is_conda_installed() -> bool:
    """Checks if conda is installed.

    Returns:
        bool: True if conda is installed, False otherwise.
    """
    cmd = shlex.split("conda --version")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        return False

    return True


def delete_conda_env(env_name: str):
    """Deletes a conda environment with the given name.

    Args:
        env_name: The name of the environment to be deleted.
    """
    cmd = shlex.split(f"conda remove -n {env_name} --all -y")
    subprocess.run(cmd, check=True, capture_output=True)


def create_env_from_file(file: Path):
    """Creates a new conda environment from a file.

    Args:
        file: The file to create the environment from, should be a yaml file
    """
    cmd = shlex.split(f"conda env create -f {str(file)}")
    subprocess.run(cmd, check=True, capture_output=True)


def get_av_conda_envs() -> list[str]:
    """Return a list of conda environments used by auto-verify."""
    conda_envs: list[str] = []

    cmd = shlex.split("conda env list")
    result = subprocess.run(cmd, check=True, capture_output=True)

    for line in str(result.stdout.decode("utf-8")).splitlines()[2:-1]:
        env_name = line.split(maxsplit=1)[0]

        if env_name.find(AV_ENV_BASE_NAME) == 0:
            conda_envs.append(env_name)

    return conda_envs


def get_verifier_conda_env_name(verifier: str) -> str | None:
    """Returns the conda environment name for the verifier, if it exists.

    Args:
        verifier: The verifier to get the conda env name for.

    Returns:
        str | None: conda environment name, if it exists.
    """
    # TODO: Check for if this env actually exists
    return AV_ENV_BASE_NAME + verifier
