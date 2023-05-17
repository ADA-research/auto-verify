"""_sumary_."""
from pathlib import Path
from typing import IO

from ConfigSpace import Configuration


class MnbabJsonConfig:
    """Class for mn-bab JSON configs."""

    def __init__(self, json_file: IO[str]):
        """_summary_."""
        self._json_file = json_file

    @classmethod
    def from_json(cls, json_file: Path, network: Path, property: Path):
        """_summary."""
        pass  # TODO:

    @classmethod
    def from_config(cls, config: Configuration, network: Path, property: Path):
        """_summary_."""
        pass  # TODO:

    def get_json_file(self) -> IO[str]:
        """_summary_."""
        pass  # TODO:
