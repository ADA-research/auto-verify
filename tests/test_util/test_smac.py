from pathlib import Path

import pytest
from ConfigSpace import ConfigurationSpace
from smac import Scenario

from autoverify.util.instances import VerificationInstance
from autoverify.util.smac import get_scenario_dict, index_features


@pytest.fixture
def scenario(
    simple_configspace: ConfigurationSpace,
    tmp_path: Path,
) -> Scenario:
    return Scenario(
        simple_configspace,
        name="test_scenario",
        output_directory=tmp_path,
    )


def test_index_features(trivial_instances: list[VerificationInstance]):
    features = index_features(trivial_instances)

    for i, feature in enumerate(features.values()):
        assert i == int(feature[0])


def test_get_scenario_dict(
    scenario: Scenario,
    simple_configspace: ConfigurationSpace,
):
    scen_dict = get_scenario_dict(scenario)

    assert scen_dict["name"] == "test_scenario"
    assert scen_dict["configspace"] == simple_configspace
