"""_summary_."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from ConfigSpace import Configuration

from autoverify.util.verifiers import verifier_from_name


@dataclass
class ConfiguredVerifier:
    """_summary_."""

    verifier: str
    config: Configuration | Path

    def __post_init__(self):
        self.verifier_class = verifier_from_name(self.verifier)

    def is_equivalent(self, cv: ConfiguredVerifier) -> bool:
        if self.verifier != cv.verifier:
            return False

        v = verifier_from_name(self.verifier)

        return v.is_same_config(self.config, cv.config)


@dataclass
class Portfolio:
    """_summary_."""

    verifiers: list[ConfiguredVerifier] = field(default_factory=list)

    def __iter__(self) -> Iterator[ConfiguredVerifier]:
        return self.verifiers.__iter__()

    def at(self, i: int) -> ConfiguredVerifier:
        """_summary_."""
        return self.verifiers[i]

    def add(self, configured_verifier: ConfiguredVerifier):
        """_summary_."""
        self.verifiers.append(configured_verifier)

    def update(self, configured_verifiers: list[ConfiguredVerifier]):
        """Update the portfolio with new incumbents.

        Does not add configured verifiers if they are already present.

        Args:
            configured_verifiers: TODO
        """
        # TODO:
        for cv in configured_verifiers:
            pass

    # TODO:
    def to_json(self, json_file: Path = Path("portfolio.json")):
        """_summary_."""
        raise NotImplementedError

    # TODO:
    @staticmethod
    def from_json(json_file: Path):
        """_summary_."""
        raise NotImplementedError
