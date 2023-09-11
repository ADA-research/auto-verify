"""_summary_."""
import logging
import random
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import numpy as np
from ConfigSpace import Categorical, Configuration, ConfigurationSpace
from smac import AlgorithmConfigurationFacade as ACFacade
from smac import RunHistory, Scenario

from autoverify.portfolio.hydra.cost_matrix import CostMatrix
from autoverify.portfolio.portfolio import (
    ConfiguredVerifier,
    Portfolio,
    PortfolioScenario,
)
from autoverify.types import TargetFunction
from autoverify.util.resources import ResourceTracker
from autoverify.util.target_function import get_verifier_tf
from autoverify.util.verification_instance import VerificationInstance
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp import inst_bench_to_kwargs
from autoverify.verifier.verifier import CompleteVerifier

logger = logging.getLogger(__name__)


def _mean_unevaluated(costs: dict[str, float]) -> dict[str, float]:
    """Set all the np.inf values to the mean of the non inf values."""
    new_costs: dict[str, float] = {}

    evaluated_costs: list[float] = [c for c in costs.values() if c != np.inf]
    mean = float(np.mean(evaluated_costs))

    for inst, cost in costs.items():
        new_costs[inst] = mean if cost == np.inf else cost

    return new_costs


def _get_cpu_gpu_alloc(verifier: str, rt: ResourceTracker):
    cpus, gpu = rt.deduct_by_name(verifier, mock=True)

    # HACK: Need to refactor ResourceTracker
    if gpu <= 0:
        gpu = -1
    else:
        gpu = 0

    return (0, cpus - 1, gpu)


def _remap_rh_keys(
    key_map: dict[Configuration, Configuration], rh: RunHistory
) -> RunHistory:
    new_rh = RunHistory()

    for tk, tv in rh.items():
        cfg = rh.get_config(tk.config_id)
        cfg = key_map[cfg]
        new_rh.add(
            cfg,
            tv.cost,
            tv.time,
            tv.status,
            tk.instance,
            tk.seed,
            tk.budget,
            tv.starttime,
            tv.endtime,
            tv.additional_info,
        )

    return new_rh


def _get_init_kwargs(
    verifier: str, scenario: PortfolioScenario, instance: VerificationInstance
) -> dict[str, Any]:
    init_kwargs: dict[str, Any] = {}

    if scenario.vnn_compat_mode:
        assert scenario.benchmark is not None
        init_kwargs = inst_bench_to_kwargs(
            scenario.benchmark, verifier, instance
        )
    elif scenario.verifier_kwargs:
        return scenario.verifier_kwargs.get(verifier, {})

    return init_kwargs


# HACK:
def _get_simplified_network(network: Path) -> Path:
    _SIMPLIFIED_FOLDER_NAME = "onnx_simplified"
    simplified_nets_dir = network.parent.parent / _SIMPLIFIED_FOLDER_NAME
    return simplified_nets_dir / network.name


def _prep_instance(
    instance: str, verifier: str, uses_simplified_network: Iterable[str] | None
) -> str:
    if not uses_simplified_network or verifier not in uses_simplified_network:
        return instance

    verif_inst = VerificationInstance.from_str(instance)
    simple_net = _get_simplified_network(verif_inst.network)
    verif_inst = VerificationInstance(
        simple_net, verif_inst.property, verif_inst.timeout
    )

    # str() becauase mypy thinks its Any (?????)
    return str(verif_inst.as_smac_instance())


# TODO: Refactor this to use a more Strategy-like pattern
# Should be able to pass different strategies for components
# such as the configurator and updater
# Maybe capture this under a more general
class Hydra:
    """_summary_."""

    def __init__(self, pf_scenario: PortfolioScenario):
        """_summary_."""
        self._scenario = pf_scenario
        self._cost_matrix = CostMatrix()
        self._stop = False

        self._ResourceTracker = ResourceTracker(self._scenario)
        self._init_logs()

    def _init_logs(self):
        assert self._scenario.output_dir
        self._scenario.output_dir.mkdir(parents=True)
        logs_path = self._scenario.output_dir
        self._log_file = (logs_path / "hydra.log").expanduser().resolve()
        self._log_file.touch(exist_ok=False)

        file_handler = logging.FileHandler(str(self._log_file))
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def _log_iter(self, pf: Portfolio):
        logger.info(
            f"Total cost after iteration {self._iter}"
            f" = {pf.get_total_cost():.2f}, mean cost = "
            f"{pf.get_mean_cost():.2f}, median cost = "
            f"{pf.get_median_cost():.2f}"
        )
        logger.info(f"Current portfolio:\n{pf.str_compact()}")

        # TODO: Who in the PF does this best cost belong to?
        logger.debug("Cost per instance:")
        for inst, cost in pf.get_all_costs().items():
            s = inst.split(",")
            inst = s[0].split("/")[-1] + "::" + s[1].split("/")[-1]
            logger.debug(f"{inst} = {cost}")

        logger.debug(">" * 80)

    def tune_portfolio(self) -> Portfolio:
        """_summary_."""
        portfolio = Portfolio()
        self._iter = 0

        for self._iter in range(self._scenario.n_iters):
            logger.info(f"Hydra iteration {self._iter}")

            new_configs = self._configurator(portfolio)
            self._updater(portfolio, new_configs)

            self._log_iter(portfolio)

            if self._scenario.stop_early and self._stop:
                logging.info(f"Stopping in iteration {self._iter}")
                break

        return portfolio

    def _configurator(
        self, pf: Portfolio
    ) -> list[tuple[Configuration, RunHistory]]:
        # TODO: Iter > 0
        new_configs: list[tuple[Configuration, RunHistory]] = []

        for i in range(self._scenario.configs_per_iter):
            logger.info(f"Configurator iteration {i}")

            run_name = f"pick_{self._iter}_{i}"
            logger.info("Picking verifier")
            verifier = self._pick(run_name, pf)

            logger.info(f"Picked {verifier}")
            logger.info(f"Tuning {verifier}")

            run_name = f"tune_{self._iter}_{i}_{verifier}"
            tf = self._get_target_func(verifier, pf)
            config, runhist = self._tune(verifier, run_name, tf)

            new_configs.append((config, runhist))

        return new_configs

    def _pick(self, run_name: str, pf: Portfolio) -> str:
        if self._scenario.pick_budget == 0:
            logging.info("Pick budget is 0, selecting random verifier.")
            return random.choice(self._scenario.verifiers)

        verifiers: list[str] = self._ResourceTracker.get_possible()

        def hydra_tf(config: Configuration, instance: str, seed: int) -> float:
            seed += 1  # silence warning
            verifier = verifiers[config["index"]]
            assert isinstance(verifier, str)

            print("<" * 40)
            print(verifier)
            print(instance)
            instance = _prep_instance(
                instance, verifier, self._scenario.uses_simplified_network
            )
            print("<" * 40)

            verifier_class = verifier_from_name(verifier)
            init_kwargs = _get_init_kwargs(
                verifier,
                self._scenario,
                VerificationInstance.from_str(instance),
            )
            alloc = _get_cpu_gpu_alloc(verifier, self._ResourceTracker)
            verifier_inst = verifier_class(
                cpu_gpu_allocation=alloc, **init_kwargs
            )

            verifier_tf = get_verifier_tf(verifier_inst)

            assert isinstance(verifier_inst, CompleteVerifier)
            cost = verifier_tf(verifier_inst.default_config, instance, seed)

            if self._iter == 0:
                return cost
            else:
                pf_cost = pf.get_cost(instance)

            return float(min(cost, pf_cost))

        walltime_limit = (
            self._scenario.seconds_per_iter
            * self._scenario.pick_budget
            / self._scenario.configs_per_iter
        )

        pick_cfgspace = ConfigurationSpace()
        pick_cfgspace.add_hyperparameter(
            Categorical(
                "index",
                [i for i in range(len(verifiers))],
                default=0,
            )
        )

        smac_scenario = Scenario(
            pick_cfgspace,
            walltime_limit=walltime_limit,
            n_trials=sys.maxsize,  # we use walltime_limit
            name=run_name,
            **self._scenario.get_smac_scenario_kwargs(),
        )

        smac = ACFacade(smac_scenario, hydra_tf, overwrite=True)
        inc = smac.optimize()

        # Not dealing with > 1 config
        assert isinstance(inc, Configuration)

        key_map: dict[Configuration, Configuration] = {}
        for i in range(len(verifiers)):
            cfg = Configuration(pick_cfgspace, {"index": i})
            key_map[cfg] = verifier_from_name(verifiers[i])().default_config

        rh = _remap_rh_keys(key_map, smac.runhistory)
        self._cost_matrix.update_matrix(rh)

        return str(verifiers[inc["index"]])

    def _tune(
        self, verifier: str, run_name: str, target_func: TargetFunction
    ) -> tuple[Configuration, RunHistory]:
        verifier_inst = verifier_from_name(verifier)()

        if self._scenario.tune_budget == 0:
            logger.info("Tune budget is 0, returning default configuration.")
            return verifier_inst.default_config, RunHistory()

        walltime_limit = (
            self._scenario.seconds_per_iter
            * self._scenario.tune_budget
            / self._scenario.configs_per_iter
        )

        smac_scenario = Scenario(
            verifier_inst.config_space,
            walltime_limit=walltime_limit,
            n_trials=sys.maxsize,  # we use walltime_limit
            name=run_name,
            **self._scenario.get_smac_scenario_kwargs(),
        )

        smac = ACFacade(smac_scenario, target_func, overwrite=True)
        inc = smac.optimize()

        # Not dealing with > 1 config
        assert isinstance(inc, Configuration)
        return inc, smac.runhistory

    def _get_target_func(self, verifier: str, pf: Portfolio) -> TargetFunction:
        """If iteration > 0, use the Hydra target function."""
        verifier_class = verifier_from_name(verifier)
        name = str(verifier_class.name)

        def hydra_tf(config: Configuration, instance: str, seed: int) -> float:
            seed += 1  # silence warning

            instance = _prep_instance(
                instance, verifier, self._scenario.uses_simplified_network
            )

            init_kwargs = _get_init_kwargs(
                name, self._scenario, VerificationInstance.from_str(instance)
            )
            alloc = _get_cpu_gpu_alloc(verifier, self._ResourceTracker)
            verifier_inst = verifier_class(
                cpu_gpu_allocation=alloc, **init_kwargs
            )
            verifier_tf = get_verifier_tf(verifier_inst)

            assert isinstance(verifier_inst, CompleteVerifier)
            cost = verifier_tf(config, instance, seed)

            if self._iter == 0:
                return cost
            else:
                pf_cost = pf.get_cost(instance)

            return float(min(cost, pf_cost))

        return hydra_tf

    # TODO: Support for adding > 1 config per iter
    def _updater(
        self,
        pf: Portfolio,
        new_configs: list[tuple[Configuration, RunHistory]],
    ):
        logger.info("Updating portfolio")

        # TODO: Actually use the cost matrix for determining
        # the initial config in the SMAC process
        for _, rh in new_configs:
            self._cost_matrix.update_matrix(rh)

        cfg = new_configs[0][0]
        # ConfigSpace name is optional, but we require it to
        # make a distinction between the different verifiers
        name = cfg.config_space.name
        assert name is not None

        cv = ConfiguredVerifier(
            name, cfg, self._ResourceTracker.deduct_by_name(name, mock=True)
        )
        if cv in pf:
            logger.info(f"Config {cv} already in portfolio")
            if self._scenario.stop_early:
                self._stop = True
                return

        pf.add(cv)

        # Re calculate the cost of the pf
        vbs_cost = _mean_unevaluated(
            self._cost_matrix.vbs_cost(
                pf.configs, self._scenario.get_smac_instances()
            )
        )

        pf.update_costs(vbs_cost)
        self._ResourceTracker.deduct_by_name(name)
