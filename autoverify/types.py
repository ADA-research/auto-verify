"""_summary_."""
# from dataclasses import dataclass, field
from typing import Callable, Sequence

from ConfigSpace import Configuration

# TODO: This is dumb, just use normal types
Instance = str
Cost = float
Seed = int

TargetFunction = Callable[[Configuration, Instance, Seed], Cost]

CostDict = dict[Instance, dict[Configuration, list[Cost]]]


VerifierResources = tuple[str, int, int]
ResourceList = Sequence[VerifierResources]
