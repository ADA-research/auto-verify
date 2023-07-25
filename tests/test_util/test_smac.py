import pytest
from ConfigSpace import ConfigurationSpace
from smac import Scenario


@pytest.fixture
def scenario(simple_configspace: ConfigurationSpace) -> Scenario:
    return Scenario(
        simple_configspace,
        name="test_scenario",
    )
