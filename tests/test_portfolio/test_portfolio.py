import pytest
from ConfigSpace import Configuration, ConfigurationSpace

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio


@pytest.fixture
def pf_cfg(simple_configspace: ConfigurationSpace) -> Configuration:
    return simple_configspace.sample_configuration()


@pytest.fixture
def portfolio(pf_cfg: Configuration) -> Portfolio:
    pf = Portfolio()
    pf.add(ConfiguredVerifier("foo", pf_cfg))
    pf.update_costs({"bar": 42.0})
    pf.update_costs({"foobar": 7.0})

    return pf


def test_get_cost(portfolio: Portfolio):
    cost = portfolio.get_cost("bar")
    assert cost == 42.0

    costs = portfolio.get_costs(["bar", "foobar"])
    assert costs == {"bar": 42.0, "foobar": 7.0}

    with pytest.raises(KeyError):
        portfolio.get_cost("hello world")
