"""_summary_."""
import logging
import random
import sys
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
from autoverify.util.target_function import get_pick_tf, get_verifier_tf
from autoverify.util.verifiers import verifier_from_name
from autoverify.verifier.verifier import CompleteVerifier, Verifier

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
    verifier: str, scenario: PortfolioScenario
) -> dict[str, Any]:
    init_kwargs: dict[str, Any] = {}  # TODO: Type

    if (
        scenario.verifier_kwargs is not None
        and verifier in scenario.verifier_kwargs
    ):
        init_kwargs = scenario.verifier_kwargs[verifier]

    return init_kwargs


# TODO: Refactor this to use a more "Strategy"-like pattern
class Hydra:
    """_summary_."""

    # hydra_iter, configurator_iter, verifier_name
    _SMAC_NAME = "hydra_{}_{}_{}"

    def __init__(self, pf_scenario: PortfolioScenario):
        """_summary_."""
        self._scenario = pf_scenario
        self._cost_matrix = CostMatrix()
        self._stop = False

        self._ResourceTracker = ResourceTracker(self._scenario)

    def tune_portfolio(self) -> Portfolio:
        """_summary_."""
        portfolio = Portfolio()
        self._iter = 0

        for self._iter in range(self._scenario.n_iters):
            logger.info(f"Hydra iteration {self._iter}")

            new_configs = self._configurator(portfolio)
            self._updater(portfolio, new_configs)

            logger.info(
                f"Total cost after iteration {self._iter}"
                f" = {portfolio.get_total_cost():.2f}, mean cost = "
                f"{portfolio.get_mean_cost():.2f}"
            )

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
            logger.info(f"Configuration iteration {i}")

            run_name = f"pick_{self._iter}_{i}"
            logger.info("Picking verifier")
            verifier = self._pick(run_name)

            logger.info(f"Picked {verifier}")
            logger.info(f"Tuning {verifier}")

            run_name = self._SMAC_NAME.format(self._iter, i, verifier)
            tf = self._get_target_func(verifier, pf)
            config, runhist = self._tune(verifier, run_name, tf)

            new_configs.append((config, runhist))

        return new_configs

    # TODO: fix type errors
    def _pick(self, run_name: str) -> str:
        if self._scenario.pick_budget == 0:
            logging.info("Pick budget is 0, selecting random verifier.")
            return random.choice(self._scenario.verifiers)

        verifier_insts: list[Verifier] = []

        for name in self._ResourceTracker.get_possible():
            verifier_class = verifier_from_name(name)
            alloc = _get_cpu_gpu_alloc(name, self._ResourceTracker)
            init_kwargs = _get_init_kwargs(name, self._scenario)
            verifier_insts.append(
                verifier_class(cpu_gpu_allocation=alloc, **init_kwargs)
            )

        target_func = get_pick_tf(verifier_insts)
        pick_cfgspace = ConfigurationSpace()
        pick_cfgspace.add_hyperparameter(
            Categorical(
                "index",
                [i for i in range(len(verifier_insts))],
                default=0,
            )
        )

        walltime_limit = (
            self._scenario.seconds_per_iter
            * self._scenario.pick_budget
            / self._scenario.configs_per_iter
        )

        smac_scenario = Scenario(
            pick_cfgspace,
            walltime_limit=walltime_limit,
            n_trials=sys.maxsize,  # we use walltime_limit
            name=run_name,
            **self._scenario.get_smac_scenario_kwargs(),
        )

        smac = ACFacade(smac_scenario, target_func, overwrite=True)
        inc = smac.optimize()

        # Not dealing with > 1 config
        assert isinstance(inc, Configuration)

        key_map: dict[Configuration, Configuration] = {}
        for i in range(len(verifier_insts)):
            cfg = Configuration(pick_cfgspace, {"index": i})
            key_map[cfg] = verifier_insts[i].default_config

        rh = _remap_rh_keys(key_map, smac.runhistory)
        self._cost_matrix.update_matrix(rh)

        return str(verifier_insts[inc["index"]].name)

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
        init_kwargs = _get_init_kwargs(name, self._scenario)
        alloc = _get_cpu_gpu_alloc(verifier, self._ResourceTracker)
        verifier_inst = verifier_class(cpu_gpu_allocation=alloc, **init_kwargs)
        verifier_tf = get_verifier_tf(verifier_inst)

        if self._iter == 0:
            return verifier_tf

        def hydra_tf(config: Configuration, instance: str, seed: int) -> float:
            seed += 1  # silence warning

            assert isinstance(verifier_inst, CompleteVerifier)
            cost = verifier_tf(config, instance, seed)
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
        assert cfg.config_space.name is not None

        cv = ConfiguredVerifier(cfg.config_space.name, cfg)
        if cv in pf:
            logger.info(f"Config {cv} already in portfolio")
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
        self._ResourceTracker.deduct_by_name(cfg.config_space.name)
