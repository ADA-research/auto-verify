"""_summary_."""
from enum import Enum


# HACK: Can't put this in `resources.py` because
# it results in a circular import
class ResourceStrategy(Enum):
    Auto = "auto"
    Exact = "exact"
