import logging
import sys
from pathlib import Path

from ConfigSpace import Configuration
from smac import AlgorithmConfigurationFacade, Scenario

from autoverify.util.smac import index_features
from autoverify.util.target_function import get_verifier_tf
from autoverify.verifier.verifier import Verifier

logger = logging.getLogger(__name__)


def smac_tune_verifier(
    verifier: Verifier,
    instances: list[str],
    walltime_limit: int,
    *,
    output_dir: Path | None = Path("tune_verifier/"),
    config_out: Path | None = Path("incumbent.txt"),
) -> Configuration:
    """_summary_."""
    if output_dir is None:
        output_dir = Path("tune_verifier/")

    if config_out is None:
        config_out = Path("incumbent.txt")

    scenario = Scenario(
        verifier.config_space,
        instances=instances,
        instance_features=index_features(instances),
        walltime_limit=walltime_limit,
        output_directory=output_dir,
        n_trials=sys.maxsize,
    )

    target_function = get_verifier_tf(verifier)

    smac = AlgorithmConfigurationFacade(
        scenario, target_function, overwrite=True
    )

    logger.info(
        f"Tuning {verifier.name} with walltime_limit={str(walltime_limit)} "
        f"on {len(instances)} instances with, "
        f"out_dir={output_dir.name} and cfg_out={config_out.name}"
    )

    inc = smac.optimize()

    # Not dealing with > 1 config
    if isinstance(inc, list):
        inc = inc[0]

    logger.info(f"Finished tuning {verifier.name}")
    logger.info(f"Got configuration:\n{inc}")
    logger.info(f"Writing incumbent configuration to {config_out.name}")

    with open(str(config_out), "w") as f:
        f.write(str(inc))

    return inc
