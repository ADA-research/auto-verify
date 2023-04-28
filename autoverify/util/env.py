"""Utilities for managing environments."""
import os
import shutil
from contextlib import contextmanager
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

    shutil.copy(file_path / "environment.yml", install_dir / "environment.yml")


@contextmanager
def environment(**env: str):
    """Temporarily set env vars and restore values aferwards."""
    original_env = {key: os.getenv(key) for key in env}
    os.environ.update(env)

    try:
        yield
    finally:
        for key, value in original_env.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value
