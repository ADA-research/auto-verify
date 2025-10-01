"""_summary_."""

import logging
import sys
from pathlib import Path

from ConfigSpace import Configuration
from smac import AlgorithmConfigurationFacade, Scenario

from autoverify.util.smac import index_features, runhistory_to_csv
from autoverify.util.target_function import get_verifier_tf, get_vnn_verifier_tf
from autoverify.util.verifiers import verifier_from_name
from autoverify.verifier.verifier import Verifier

logger = logging.getLogger(__name__)


def vnn_smac_tune_verifier(
    verifier: str,
    instances: list[str],
    benchmark: str,
    walltime_limit: int,
    *,
    run_name: str | None = None,
    output_dir: Path | None = Path("tune_verifier_vnn/"),
    config_out: Path | None = Path("incumbent.txt"),
    rh_csv_path: Path | None = Path("runhistory.csv"),
) -> Configuration:
    """_summary_."""
    if output_dir is None:
        output_dir = Path("tune_verifier/")

    if config_out is None:
        config_out = Path("incumbent.txt")

    verifier_inst = verifier_from_name(verifier)()
    cfg_space = verifier_inst.config_space
    name = verifier_inst.name

    scenario = Scenario(
        cfg_space,
        name=run_name,
        instances=instances,
        instance_features=index_features(instances),
        walltime_limit=walltime_limit,
        output_directory=output_dir,
        n_trials=sys.maxsize,
    )

    target_function = get_vnn_verifier_tf(verifier, benchmark)

    smac = AlgorithmConfigurationFacade(scenario, target_function, overwrite=True)

    logger.info(
        f"Tuning {name} with walltime_limit={str(walltime_limit)} "
        f"on {len(instances)} instances with, "
        f"out_dir={output_dir.name} and cfg_out={config_out.name}"
    )

    inc = smac.optimize()

    # Not dealing with > 1 config
    if isinstance(inc, list):
        inc = inc[0]

    logger.info(f"Finished tuning {name}")
    logger.info(f"Got configuration:\n{inc}")
    logger.info(f"Writing incumbent configuration to {str(config_out)}")

    with open(str(config_out), "w") as f:
        f.write(str(inc))

    if rh_csv_path:
        logger.info(f"Writing RunHistory to {str(rh_csv_path)}")
        runhistory_to_csv(smac.runhistory, rh_csv_path)

    return inc


def smac_tune_verifier(
    verifier: Verifier,
    instances: list[str],
    walltime_limit: int,
    *,
    output_dir: Path | None = Path("tune_verifier/"),
    config_out: Path | None = Path("incumbent.txt"),
    run_name: str | None = None,
    rh_csv_path: Path | None = None,
) -> Configuration:
    """_summary_."""
    if output_dir is None:
        output_dir = Path("tune_verifier/")

    if config_out is None:
        config_out = Path("incumbent.txt")

    scenario = Scenario(
        verifier.config_space,
        name=run_name,
        instances=instances,
        instance_features=index_features(instances),
        walltime_limit=walltime_limit,
        output_directory=output_dir,
        n_trials=sys.maxsize,
    )

    target_function = get_verifier_tf(verifier)

    smac = AlgorithmConfigurationFacade(scenario, target_function, overwrite=True)

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
    logger.info(f"Writing incumbent configuration to {str(config_out)}")

    with open(str(config_out), "w") as f:
        f.write(str(inc))

    if rh_csv_path:
        logger.info(f"Writing RunHistory to {str(rh_csv_path)}")
        runhistory_to_csv(smac.runhistory, rh_csv_path)

    return inc
