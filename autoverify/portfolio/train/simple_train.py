"""_summary_."""
from typing import Any

from ConfigSpace import Configuration
from smac import HyperparameterOptimizationFacade, Scenario

from autoverify.portfolio.target_function import SmacTargetFunction


def smac_train(
    scenario: Scenario,
    target_function: SmacTargetFunction,
    **smac_facade_kwargs: Any,
) -> Configuration:
    """_summary_."""
    smac = HyperparameterOptimizationFacade(
        scenario, target_function, **smac_facade_kwargs
    )
    incumbent = smac.optimize()
    return incumbent
