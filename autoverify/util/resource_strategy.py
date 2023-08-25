"""_summary_."""
from enum import Enum


# HACK: Can't put this in `resources.py` because
# it results in a circular import
class ResourceStrategy(Enum):
    """_summary_."""

    Auto = "auto"
    Exact = "exact"
