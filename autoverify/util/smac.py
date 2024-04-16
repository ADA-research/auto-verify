"""SMAC util."""

import copy
import csv
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any

from smac import RunHistory, Scenario
from smac.runhistory.dataclasses import TrialKey, TrialValue

from autoverify.util.dataclass import get_dataclass_field_names
from autoverify.util.verification_instance import VerificationInstance


def get_smac_run_data(run_folder: Path) -> dict[str, Any]:
    """Get some data about from the SMAC logs."""
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
    """Get a SMAC scneario as a dict."""
    config_space = copy.deepcopy(scenario.configspace)

    # Need to edit the output directory, but scenario dataclass is frozen
    scenario_dict = Scenario.make_serializable(scenario)

    # Configspace is removed during serialization so add it back
    scenario_dict["configspace"] = config_space

    # _meta can't be in the init kwargs
    scenario_dict.pop("_meta", None)

    return scenario_dict  # type: ignore


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
