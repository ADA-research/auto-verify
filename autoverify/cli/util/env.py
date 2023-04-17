"""Utilities for managing environments."""
import os
import shutil
from pathlib import Path


def get_file_path(file: Path) -> Path:
    """Returns the absolute path to the file.

    Args:
        file: The file to get the path to.

    Returns:
        Path: The path to the file.
    """
    return Path(
        os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(file)))
    )


def copy_env_file_to(installer_py_file: Path, install_dir: Path):
    """Copies the env file to a location.

    Args:
        installer_py_file: The path to the installer directory (e.g. nnenum),
            this is used to find the `conda_env.yml` file.
        install_dir: The directory the file is copied to.
    """
    file_path = get_file_path(installer_py_file)

    shutil.copy(file_path / "conda_env.yml", install_dir / "conda_env.yml")
