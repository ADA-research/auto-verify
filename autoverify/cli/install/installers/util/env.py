"""Util functions for creating conda envs."""
import os
from pathlib import Path


def create_env_file(location: Path):
    os.chdir(location)
    os.mknod("env.yml")
