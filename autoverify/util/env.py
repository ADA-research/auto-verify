"""Utilities for managing environments."""
import os
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path

from autoverify.util.proc import pkill_match


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


@contextmanager
def cwd(path: Path):
    """Change the current working directory (cwd) and restore it afterwards.

    Args:
        path: The path that will be set as the cwd.
    """
    old_wd = os.getcwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(old_wd)


@contextmanager
def sys_path(path: Path):
    """Temporarily modify the system PATH."""
    fs_path = str(path)

    try:
        sys.path.insert(0, fs_path)
        yield
    finally:
        sys.path.remove(fs_path)


@contextmanager
def pkill_match_list(matches: list[str]):
    """Kill a list of process name patterns when exiting context."""
    try:
        yield
    finally:
        for match in matches:
            pkill_match(match)
