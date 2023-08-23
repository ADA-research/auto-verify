from copy import copy

import pytest

from autoverify.portfolio.portfolio import PortfolioScenario
from autoverify.util.resource_strategy import ResourceStrategy
from autoverify.util.resources import ResourceTracker
from autoverify.util.verification_instance import VerificationInstance

# TODO: Mock number of CPUs and GPUs


@pytest.fixture
def resource_tracker(
    trivial_instances: list[VerificationInstance],
) -> ResourceTracker:
    pf_scen = PortfolioScenario(
        ["nnenum", "verinet"],
        [
            ("nnenum", 0, 0),
            ("verinet", 0, 1),  # cpus dont matter for auto
        ],
        trivial_instances,
        2,
        1,
        configs_per_iter=1,
        alpha=1,
    )

    rt = ResourceTracker(pf_scen, strategy=ResourceStrategy.Auto)
    return rt


def test_get_possible(resource_tracker: ResourceTracker):
    p = resource_tracker.get_possible()
    assert "nnenum" in p
    assert "verinet" in p


def test_deduct(resource_tracker: ResourceTracker):
    pre_cpu, pre_gpu = copy(resource_tracker.resources)
    resource_tracker.deduct((0, 1))
    assert resource_tracker._resources == (pre_cpu, pre_gpu - 1)
    resource_tracker.deduct((8, 0))
    assert resource_tracker._resources == (pre_cpu - 8, pre_gpu - 1)

    p = resource_tracker.get_possible()
    assert "nnenum" in p
    assert "verinet" not in p


def test_deduct_from_name(resource_tracker: ResourceTracker):
    pre_cpu, pre_gpu = copy(resource_tracker.resources)

    resource_tracker.deduct_from_name("nnenum")
    assert resource_tracker.resources == (pre_cpu / 2, pre_gpu)

    resource_tracker.deduct_from_name("verinet")
    assert resource_tracker.resources == (0, pre_gpu - 1)
