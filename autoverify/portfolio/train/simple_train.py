"""_summary_."""
from typing import Any, Callable

from ConfigSpace import Configuration
from hydrasmac import Hydra
from smac import HyperparameterOptimizationFacade, Scenario

from autoverify.verifier.verifier import Verifier

SmacTargetFunction = Callable[[Configuration, str, int], float]


def target_function(
    config: Configuration, instance: str, seed: int = 0
) -> float:
    return 1.0


# TODO: Return type
def train_portfolio(*verifiers: Verifier, some_param: int = 10):
    print(verifiers)
    print(some_param)
    return


# TODO: Return type
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
