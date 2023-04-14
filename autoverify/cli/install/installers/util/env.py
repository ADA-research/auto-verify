import os
import shutil
from pathlib import Path


def get_file_path(file: str) -> str:
    """Returns the absolute path to the file."""
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(file)))


def copy_env_file(src: Path, dst: Path):
    shutil.copy(src, dst)
