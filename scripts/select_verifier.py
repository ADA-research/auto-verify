from pathlib import Path

from smac import HyperparameterOptimizationFacade, Scenario

from autoverify.portfolio.select_verifier_configspace import (
    make_select_verifier_configspace,
)
from autoverify.portfolio.target_function import (
    make_pick_verifier_target_function,
)
from autoverify.util.env import get_file_path
from autoverify.util.instances import (
    read_vnncomp_instances,
    verification_instances_to_smac_instances,
)
from autoverify.verifier import AbCrown, Nnenum, OvalBab

from .util import mnist_features

if __name__ == "__main__":
    mnist_instances = read_vnncomp_instances("mnist_fc")
    file_path = get_file_path(Path(__file__))

    mnist_features = mnist_features(mnist_instances)

    verifiers = [AbCrown, Nnenum, OvalBab]
    config_space = make_select_verifier_configspace(verifiers)
    target_function = make_pick_verifier_target_function()

    scenario = Scenario(
        config_space,
        walltime_limit=180,
        instances=verification_instances_to_smac_instances(mnist_instances),
        instance_features=mnist_features,
    )

    smac = HyperparameterOptimizationFacade(
        scenario,
        target_function,
        overwrite=True,
    )
    inc = smac.optimize()
    print(inc)
