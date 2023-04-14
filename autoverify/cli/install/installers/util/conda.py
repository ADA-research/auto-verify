"""Conda utility functions."""

import shlex
import subprocess
from pathlib import Path


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


def create_env_from_file(file: Path):
    """Creates a new conda environment from a file.

    Args:
        file: The file to create the environment from, should be a yaml file
    """
    cmd = shlex.split(f"conda env create -f {str(file)}")
    subprocess.run(cmd, check=True, capture_output=True)
