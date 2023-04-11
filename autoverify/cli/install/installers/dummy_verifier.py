"""_summary_."""
import os
from pathlib import Path


def install(install_dir: Path):
    """_summary_."""
    os.mknod(install_dir / "test")
