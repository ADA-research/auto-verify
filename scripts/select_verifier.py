from pathlib import Path

from smac import HyperparameterOptimizationFacade, Scenario

from autoverify.portfolio.select_verifier_configspace import (
    make_select_verifier_configspace,
)
from autoverify.portfolio.target_function import (
    make_select_verifier_target_function,
)
from autoverify.util.env import get_file_path
from autoverify.util.instances import (
    VerificationInstance,
    read_vnncomp_instances,
    verification_instances_to_smac_instances,
)
from autoverify.verifier import AbCrown, Nnenum, OvalBab


def get_mnist_features(
    mnist_instances: list[VerificationInstance],
) -> dict[str, list[float]]:
    features = {}

    for inst in mnist_instances:
        size = inst.network.name.split(".")[0][-1]
        features[inst.as_smac_instance()] = [float(size)]

    return features


if __name__ == "__main__":
    mnist_instances = read_vnncomp_instances("mnist_fc")
    file_path = get_file_path(Path(__file__))

    mnist_features = get_mnist_features(mnist_instances)
    mnist_instances = verification_instances_to_smac_instances(mnist_instances)

    verifiers = [AbCrown, Nnenum, OvalBab]
    config_space = make_select_verifier_configspace(verifiers)
    target_function = make_select_verifier_target_function()

    scenario = Scenario(
        config_space,
        walltime_limit=180,
        instances=mnist_instances,
        instance_features=mnist_features,
    )

    smac = HyperparameterOptimizationFacade(
        scenario,
        target_function,
        overwrite=True,
    )
    inc = smac.optimize()
    print(inc)
