import pytest

from autoverify.util.resource_strategy import (
    ResourceStrategy,
    resources_from_strategy,
)


def test_resources_from_strategy():
    resources = resources_from_strategy(
        ResourceStrategy.Auto, ["nnenum", "verinet", "abcrown"]
    )
    assert resources == [
        ("nnenum", 0, 0),
        ("verinet", 0, 1),
        ("abcrown", 0, 1),
    ]

    with pytest.raises(NotImplementedError):
        resources_from_strategy(ResourceStrategy.Exact, ["nnenum"])
