import copy
from pathlib import Path
from typing import Any

from smac.scenario import Scenario


def get_scenario_dict(scenario: Scenario) -> dict[str, Any]:
    """TODO Docstring"""
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
    """TODO Docstring"""
    scenario_dict = get_scenario_dict(scenario)

    scenario_dict["output_directory"] = output_dir
    scenario_dict["name"] = name

    return Scenario(**scenario_dict)


def set_scenario_instances(
    scenario: Scenario,
    instances: list[str],
    instance_features: dict[str, list[float]],
) -> Scenario:
    """TODO Docstring"""
    scenario_dict = get_scenario_dict(scenario)

    scenario_dict["instances"] = instances
    scenario_dict["instance_features"] = instance_features

    return Scenario(**scenario_dict)
