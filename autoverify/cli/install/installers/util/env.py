"""Util functions for creating conda envs."""
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CondaEnv:
    name: str
    channels: list[str] | None
    dependencies: list[str] | None

    def write_to_yaml(self, file: Path):
        pass


def create_empty_env_file(dir: Path):
    os.mknod(dir / "environment.yml")
