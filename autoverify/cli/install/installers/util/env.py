"""Util functions for creating conda envs."""
import os
from pathlib import Path


def create_env_file(dir: Path):
    os.mknod(dir / "environment.yml")
