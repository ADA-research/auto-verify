import pytest
from ConfigSpace import Configuration, ConfigurationSpace

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio


@pytest.fixture
def pf_cfg(simple_configspace: ConfigurationSpace) -> Configuration:
    return simple_configspace.sample_configuration()


@pytest.fixture
def pf_cfg2(simple_configspace: ConfigurationSpace) -> Configuration:
    return simple_configspace.sample_configuration()


@pytest.fixture
def portfolio(pf_cfg: Configuration, pf_cfg2: Configuration) -> Portfolio:
    pf = Portfolio()
    pf.add(ConfiguredVerifier("foo", pf_cfg, resources=(8, 0)))
    pf.add(ConfiguredVerifier("hello", pf_cfg2, resources=(8, 1)))
    pf.update_costs({"bar": 42.0})
    pf.update_costs({"foobar": 7.0})

    return pf
