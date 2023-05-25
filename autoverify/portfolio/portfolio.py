"""_summary_."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from ConfigSpace import Configuration

from autoverify.verifier.complete.nnenum.nnenum_verifier import Nnenum
from autoverify.verifier.verifier import CompleteVerifier

ConfiguredVerifier = tuple[type[CompleteVerifier], Configuration | Path]


# TODO: Dont allow duplicates in verifiers
@dataclass
class Portfolio:
    """_summary_."""

    verifiers: list[ConfiguredVerifier] = field(default_factory=list)

    def __iter__(self) -> Iterator[ConfiguredVerifier]:
        return self.verifiers.__iter__()

    def add(self, configured_verifier: ConfiguredVerifier):
        """_summary_."""
        self.verifiers.append(configured_verifier)

    # TODO:
    def to_json(self, json_file: Path = Path("portfolio.json")):
        """_summary_."""
        raise NotImplementedError

    # TODO:
    @classmethod
    def from_json(cls, json_file: Path):
        """_summary_."""
        raise NotImplementedError
