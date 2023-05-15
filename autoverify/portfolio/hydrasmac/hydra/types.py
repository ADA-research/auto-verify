"""Hydra types."""
from typing import Callable

from ConfigSpace import Configuration

CostDict = dict[str, float]
TargetFunction = Callable[[Configuration, str, int], float]
