"""_summary_."""

from typing import Any

from ConfigSpace import Configuration
from hydrasmac import Hydra
from smac import Scenario

from autoverify.portfolio.target_function import SmacTargetFunction


def hydra_train(
    scenario: Scenario,
    target_function: SmacTargetFunction,
    **hydra_kwargs: Any,
) -> list[Configuration]:
    smac = Hydra(scenario, target_function, **hydra_kwargs)
    incumbents = smac.optimize()
    return incumbents
