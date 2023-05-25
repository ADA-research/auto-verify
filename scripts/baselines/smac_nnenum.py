from smac import AlgorithmConfigurationFacade, Scenario

from autoverify.portfolio.target_function import make_verifier_target_function
from autoverify.util.instances import (
    read_vnncomp_instances,
    verification_instances_to_smac_instances,
)
from autoverify.verifier import Nnenum
from autoverify.verifier.complete.nnenum.nnenum_configspace import (
    NnenumConfigspace,
)
from scripts.util import mnist_features

mnist_instances = read_vnncomp_instances("mnist_fc")


if __name__ == "__main__":
    scenario = Scenario(
        NnenumConfigspace,
        instances=verification_instances_to_smac_instances(mnist_instances),
        instance_features=mnist_features(mnist_instances),
        walltime_limit=60 * 60 * 8,
        deterministic=False,
    )
    target_function = make_verifier_target_function(Nnenum)

    smac = AlgorithmConfigurationFacade(
        scenario,
        target_function,
        overwrite=True,
    )
    inc = smac.optimize()
    print(inc)
