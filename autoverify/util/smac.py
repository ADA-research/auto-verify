"""SMAC util."""
import copy
from pathlib import Path
from typing import Any

from smac import Scenario

from autoverify.util.instances import VerificationInstance


def index_features(
    instances: list[str] | list[VerificationInstance],
) -> dict[str, list[float]]:
    """Use indices as simple instance features."""
    features = {}

    for i, inst in enumerate(instances):
        k = inst

        if isinstance(inst, VerificationInstance):
            k = inst.as_smac_instance()

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
