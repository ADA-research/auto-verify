from smac import Scenario

from autoverify.portfolio.target_function import make_verifier_target_function
from autoverify.portfolio.train.hydra_train import hydra_train
from autoverify.util.instances import (
    VerificationInstance,
    read_vnncomp_instances,
)
from autoverify.verifier.complete import AbCrown
from autoverify.verifier.complete.abcrown.abcrown_configspace import (
    AbCrownConfigspace,
)


def filter_to_small(
    mnist_instances: list[VerificationInstance],
) -> list[str]:
    small_instances = []

    for inst in mnist_instances:
        size = inst.network.name.split(".")[0][-1]

        if size == "2":
            small_instances.append(inst.as_smac_instance())

    return small_instances


def mnist_features(mnist_instances):
    features = {}

    for inst in mnist_instances:
        size = float(inst.split(",")[0].split(".")[0][-1])
        features[inst] = [size]

    return features


if __name__ == "__main__":
    mnist_instances = read_vnncomp_instances("mnist_fc")
    target_function = make_verifier_target_function(AbCrown)
    # instances = filter_to_small(mnist_instances)

    scenario = Scenario(
        AbCrownConfigspace,
        instances=mnist_instances,
        instance_features=mnist_features(mnist_instances),
        walltime_limit=600,
        deterministic=False,
    )

    incs = hydra_train(scenario, target_function, stop_early=False)
    print(incs)
