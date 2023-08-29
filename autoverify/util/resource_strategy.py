"""_summary_."""
from enum import Enum

from autoverify.types import ResourceList
from autoverify.util.verifiers import uses_gpu


# HACK: Can't put this in `resources.py` because
# it results in a circular import
class ResourceStrategy(Enum):
    """_summary_."""

    Auto = "auto"
    Exact = "exact"


def resources_from_strategy(
    rs: ResourceStrategy, verifiers: list[str]
) -> ResourceList:
    """_summary_."""
    resources: ResourceList = []

    if rs == ResourceStrategy.Auto:
        for verifier in verifiers:
            resources.append((verifier, 0, 1 if uses_gpu(verifier) else 0))
    else:
        raise NotImplementedError(f"ResourceStrategy {rs} not supported yet.")

    return resources
