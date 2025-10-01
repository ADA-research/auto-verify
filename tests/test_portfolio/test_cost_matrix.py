import pytest
from ConfigSpace import ConfigurationSpace
from smac import RunHistory
from smac.runhistory.enumerations import StatusType

from autoverify.portfolio.hydra.cost_matrix import CostMatrix, InstanceCost


def test_update_instance_cost():
    ic = InstanceCost()
    ic.update_cost("foo", 20.0)

    assert ic["foo"] == 20.0
    assert ic._val_counts["foo"] == 1

    ic.update_cost("foo", 40.0)

    assert ic["foo"] == 30.0
    assert ic._val_counts["foo"] == 2

    ic.update_cost("bar", 100.0)
    ic.update_cost("bar", 0.0)
    ic.update_cost("bar", 0.0)

    assert ic["bar"] == 100.0 / 3


def test_update_cost_matrix(simple_configspace: ConfigurationSpace):
    cfg1, cfg2 = simple_configspace.sample_configuration(2)

    rh = RunHistory()
    rh.add(cfg1, 10.0, instance="foo")
    rh.add(cfg2, 20.0, instance="bar")

    cm = CostMatrix()
    cm.update_matrix(rh)

    assert cm[cfg1] == {"foo": 10.0}
    assert cm[cfg2] == {"bar": 20.0}

    rh = RunHistory()
    rh.add(cfg1, 5.0, instance="foo")
    rh.add(cfg1, 20.0, instance="bar")

    cm.update_matrix(rh)
    assert cm[cfg1] == {"foo": 7.5, "bar": 20.0}
    assert cm[cfg2] == {"bar": 20.0}

    rh = RunHistory()
    rh.add(cfg1, 105.0, instance="foo")
    rh.add(cfg2, 200.0, instance="bar")
    rh.add(cfg2, 200.0, instance="foo")
    rh.add(cfg2, 1000.0, instance="foo_timeout", status=StatusType.TIMEOUT)
    cm.update_matrix(rh)

    assert cm[cfg1] == {"foo": 40.0, "bar": 20.0}
    assert cm[cfg2] == {"foo": 200.0, "bar": 110.0, "foo_timeout": 10000.0}


@pytest.fixture
def small_cost_matrix(simple_configspace: ConfigurationSpace) -> CostMatrix:
    cfg1, cfg2 = simple_configspace.sample_configuration(2)

    rh = RunHistory()
    rh.add(cfg1, 10.0, instance="foo", seed=0)
    rh.add(cfg1, 30.0, instance="foo", seed=1)
    rh.add(cfg1, 1.0, instance="bar", seed=0)
    rh.add(cfg1, 5.0, instance="bar", seed=1)
    rh.add(cfg2, 1.5, instance="foo", seed=0)
    rh.add(cfg2, 20.0, instance="bar", seed=1)
    rh.add(cfg2, 42.0, instance="foobar", seed=0)

    cm = CostMatrix()
    cm.update_matrix(rh)

    return cm


def test_vbs_cost(small_cost_matrix: CostMatrix):
    instances = ["foo", "bar"]
    configs = small_cost_matrix.keys()

    vbs_cost = small_cost_matrix.vbs_cost(configs, instances)
    assert vbs_cost == {"foo": 1.5, "bar": 3.0}


def test_vbs_cost2(simple_configspace: ConfigurationSpace):
    cfg1, cfg2, cfg3, cfg4 = simple_configspace.sample_configuration(4)

    rh = RunHistory()
    rh.add(cfg1, 10.0, instance="foo", seed=0)
    rh.add(cfg2, 5.0, instance="foo", seed=0)
    rh.add(cfg3, 20.0, instance="foo", seed=0)

    cm = CostMatrix()
    cm.update_matrix(rh)

    assert cm.vbs_cost([cfg1, cfg2, cfg3], ["foo"]) == {"foo": 5.0}
    assert cm.vbs_cost([cfg1, cfg2], ["foo"]) == {"foo": 5.0}
    assert cm.vbs_cost([cfg1, cfg3], ["foo"]) == {"foo": 10.0}

    with pytest.raises(RuntimeError):
        # This config should not be in the cost matrix
        cm.vbs_cost([cfg4], ["foo"])


def test_cost_matrix_dunders(small_cost_matrix: CostMatrix, simple_configspace: ConfigurationSpace):
    new_config = simple_configspace.sample_configuration()
    small_cost_matrix[new_config] = {"foo": 1000, "bar": 1000}
    assert small_cost_matrix[new_config] == {"foo": 1000, "bar": 1000}

    del small_cost_matrix[new_config]
    assert new_config not in small_cost_matrix

    assert len(small_cost_matrix) == 2
    assert repr(small_cost_matrix) == str(small_cost_matrix)


def test_instance_cost_dunders():
    ic = InstanceCost()
    ic["foo"] = 20.0

    assert ic["foo"] == 20.0
    assert len(ic) == 1
    assert repr(ic) == str(ic)

    del ic["foo"]
    assert "foo" not in ic
