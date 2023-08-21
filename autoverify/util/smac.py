"""SMAC util."""
import copy
import csv
import json
import statistics
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any, cast

from ConfigSpace import Configuration
from smac import RunHistory, Scenario
from smac.runhistory.dataclasses import TrialKey, TrialValue

from autoverify.types import CostDict
from autoverify.util.dataclass import get_dataclass_field_names
from autoverify.util.verification_instance import VerificationInstance


def get_smac_run_data(run_folder: Path) -> dict[str, Any]:
    """_summary_."""
    data: dict[str, Any] = {}

    with open(run_folder / "runhistory.json", "r") as f:
        runhist = json.load(f)

    with open(run_folder / "intensifier.json", "r") as f:
        intensifier = json.load(f)

    data["incumbents_changed"] = intensifier["incumbents_changed"]
    data["n_runs"] = runhist["stats"]["finished"]

    data["success"] = 0
    data["crashed"] = 0
    data["timeout"] = 0
    data["memoryout"] = 0

    for run in runhist["data"]:
        if run[6] == 1:
            data["success"] += 1
        elif run[6] == 2:
            data["crashed"] += 1
        elif run[6] == 3:
            data["timeout"] += 1
        elif run[6] == 4:
            data["memoryout"] += 1

    return data


def index_features(
    instances: Sequence[str] | Sequence[VerificationInstance],
) -> dict[str, list[float]]:
    """Returns list indices as the instance features."""
    features: dict[str, list[float]] = {}

    for i, inst in enumerate(instances):
        k = inst

        if isinstance(inst, VerificationInstance):
            k = inst.as_smac_instance()

        assert isinstance(k, str)
        features[k] = [float(i)]

    return features


def get_scenario_dict(scenario: Scenario) -> dict[str, Any]:
    """TODO Docstring."""
    config_space = copy.deepcopy(scenario.configspace)

    # Need to edit the output directory, but scenario dataclass is frozen
    scenario_dict = Scenario.make_serializable(scenario)

    # Configspace is removed during serialization so add it back
    scenario_dict["configspace"] = config_space

    # _meta can't be in the init kwargs
    scenario_dict.pop("_meta", None)

    return scenario_dict  # type: ignore


def set_scenario_output_dir(
    scenario: Scenario, output_dir: Path, name: str
) -> Scenario:
    """TODO Docstring."""
    scenario_dict = get_scenario_dict(scenario)

    scenario_dict["output_directory"] = output_dir
    scenario_dict["name"] = name

    return Scenario(**scenario_dict)


def set_scenario_instances(
    scenario: Scenario,
    instances: list[str],
    instance_features: dict[str, list[float]],
) -> Scenario:
    """TODO Docstring."""
    scenario_dict = get_scenario_dict(scenario)

    scenario_dict["instances"] = instances
    scenario_dict["instance_features"] = instance_features

    return Scenario(**scenario_dict)


def costs_from_runhistory(rh: RunHistory) -> CostDict:
    """_summary_."""
    costs: CostDict = {}

    for config in rh.get_configs():
        for isb in rh.get_instance_seed_budget_keys(config, False):
            instance = isb.instance

            if instance is None:
                continue

            cost = rh.average_cost(config, [isb], normalize=True)
            cost = cast(float, cost)

            if instance not in costs:
                costs[instance] = {}

            if config not in costs[instance]:
                costs[instance][config] = []

            costs[instance][config].append(cost)

    return costs


def costs_per_inst_from_rh(
    rh: RunHistory,
    config: Configuration,
    *,
    average=True,
) -> dict[str, list[float]]:
    """_summary_."""
    costs: dict[str, list[float]] = {}

    for isb in rh.get_instance_seed_budget_keys(config):
        if isb.instance is None:
            continue

        avg_cost = rh.average_cost(config, [isb], normalize=True)
        avg_cost = cast(float, avg_cost)

        if isb.instance in costs:
            costs[isb.instance].append(avg_cost)
        else:
            costs[isb.instance] = [avg_cost]

    if average:
        for inst, cost_list in costs.items():
            costs[inst] = [statistics.mean(cost_list)]

    return costs


def runhistory_to_csv(rh: RunHistory, csv_path: Path):
    """Write a RunHistory object to a CSV file."""
    key_header = get_dataclass_field_names(TrialKey)
    value_header = get_dataclass_field_names(TrialValue)

    with open(csv_path.expanduser().resolve(), "w") as f:
        writer = csv.DictWriter(f, fieldnames=key_header + value_header)
        writer.writeheader()

        for trial_info, trial_value in rh.items():
            row_dict = asdict(trial_info)
            row_dict.update(asdict(trial_value))
            writer.writerow(row_dict)
