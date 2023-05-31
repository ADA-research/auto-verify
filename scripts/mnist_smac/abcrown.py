import logging
import sys
from pathlib import Path

from smac import AlgorithmConfigurationFacade, Scenario

from autoverify.portfolio.target_function import make_verifier_target_function
from autoverify.util.instances import (
    read_vnncomp_instances,
    verification_instances_to_smac_instances,
)
from autoverify.util.smac import index_features
from autoverify.verifier import AbCrown
from autoverify.verifier.complete.abcrown import AbCrownConfigspace

logger = logging.getLogger(__name__)
mnist_fc = read_vnncomp_instances("mnist_fc")

if __name__ == "__main__":
    output_dir = Path(sys.argv[1])
    cfg_out = Path(sys.argv[2])

    scenario = Scenario(
        AbCrownConfigspace,
        instances=verification_instances_to_smac_instances(mnist_fc),
        instance_features=index_features(mnist_fc),
        walltime_limit=60,
        deterministic=True,
        output_directory=output_dir,
    )

    target_function = make_verifier_target_function(AbCrown)

    smac = AlgorithmConfigurationFacade(
        scenario, target_function, overwrite=True
    )

    inc = smac.optimize()

    inc = str(inc)
    logger.info(f"Incumbent:\n{inc}")

    with open(str(cfg_out), "w") as f:
        f.write(inc)
