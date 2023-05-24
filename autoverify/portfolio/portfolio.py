"""_summary_."""
from pathlib import Path

from ConfigSpace import Configuration

from autoverify.verifier.verifier import CompleteVerifier

# TODO: Proper (data)class
# FIXME: This gives type errors when doing something like:
# portfolio = [(Nnenum, None)]
Portfolio = list[tuple[type[CompleteVerifier], Configuration | Path | None]]
