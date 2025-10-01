import csv
from pathlib import Path

import pytest
from ConfigSpace import ConfigurationSpace
from smac import RunHistory, Scenario

from autoverify.util.instances import VerificationInstance
from autoverify.util.smac import (
    get_scenario_dict,
    get_smac_run_data,
    index_features,
    runhistory_to_csv,
)


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


@pytest.fixture
def runhistory(simple_configspace: ConfigurationSpace) -> RunHistory:
    cfg1, cfg2 = simple_configspace.sample_configuration(2)

    rh = RunHistory()
    rh.add(cfg1, 10.0, instance="foo")
    rh.add(cfg2, 20.0, instance="bar")

    return rh


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


def test_rh_to_csv(runhistory: RunHistory, tmp_path: Path):
    csv_file = tmp_path / "rh.csv"
    runhistory_to_csv(runhistory, csv_file)

    with open(csv_file) as f:
        reader = csv.DictReader(f)

        rows = list(reader)
        assert rows[0]["instance"] == "foo"
        assert float(rows[0]["cost"]) == 10.0
        assert rows[1]["instance"] == "bar"
        assert float(rows[1]["cost"]) == 20.0


def test_get_smac_run_data():
    data = get_smac_run_data(Path(__file__).parent / "some_runhistory")
    assert data == {
        "incumbents_changed": 1,
        "n_runs": 10,
        "success": 7,
        "crashed": 1,
        "timeout": 1,
        "memoryout": 1,
    }
