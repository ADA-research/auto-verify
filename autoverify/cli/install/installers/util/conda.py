"""Conda utility functions."""

import shlex
import subprocess
from pathlib import Path


def is_conda_installed() -> bool:
    cmd = shlex.split("conda --version")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        return False

    return True


def create_env_from_file(file: Path):
    cmd = shlex.split(f"conda env create -f {str(file)}")
    subprocess.run(cmd, check=True, capture_output=True)
