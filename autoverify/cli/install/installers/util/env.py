import os
import shutil
from pathlib import Path


def get_file_path(file: Path) -> Path:
    """Returns the absolute path to the file."""
    return Path(
        os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(file)))
    )


def copy_env_file_to(installer_py_file: Path, install_dir: Path):
    file_path = get_file_path(installer_py_file)

    shutil.copy(
        file_path / "environment.yaml", install_dir / "environment.yaml"
    )
