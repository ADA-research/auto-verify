from smac import Scenario

from autoverify.portfolio.target_function import make_verifier_target_function
from autoverify.util.instances import (
    read_vnncomp_instances,
    verification_instances_to_smac_instances,
)
from autoverify.verifier.complete import AbCrown
from autoverify.verifier.complete.abcrown.abcrown_configspace import (
    AbCrownConfigspace,
)

from ..util import filter_to_small, mnist_features

if __name__ == "__main__":
    mnist_instances = read_vnncomp_instances("mnist_fc")
    mnist_instances = verification_instances_to_smac_instances(mnist_instances)
    target_function = make_verifier_target_function(AbCrown)
    # instances = filter_to_small(mnist_instances)

    # TODO: Hydra training
    # TODO: Narrow the ab-crown searchspace some more and fix asserts/errors
    scenario = Scenario(
        AbCrownConfigspace,
        instances=mnist_instances,
        instance_features=mnist_features(mnist_instances),
        walltime_limit=600,
        deterministic=False,
    )

    incs = hydra_train(scenario, target_function, stop_early=False)
    print(incs)
