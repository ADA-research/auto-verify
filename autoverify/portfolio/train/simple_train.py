"""_summary_."""


from ConfigSpace import Configuration
from hydrasmac import Hydra
from smac import Scenario

from autoverify.verifier.verifier import Verifier


def target_function(
    config: Configuration, instance: str, seed: int = 0
) -> float:
    return 1.0


# TODO: Return type
def train_portfolio(*verifiers: Verifier, some_param: int = 10):
    print(verifiers)
    print(some_param)
    return


def train_verifier(verifier: Verifier, scenario: Scenario):
    hydra = Hydra(scenario, target_function)
