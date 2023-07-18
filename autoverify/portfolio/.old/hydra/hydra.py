"""_summary_."""
import datetime
import random
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict

from ConfigSpace import Configuration
from smac import AlgorithmConfigurationFacade, Scenario

from autoverify.portfolio.hydra.hydra_scenario import HydraScenario
from autoverify.portfolio.hydra.incumbent import Incumbent, Incumbents
from autoverify.portfolio.portfolio import Portfolio
from autoverify.portfolio.target_function import (
    SmacTargetFunction,
    make_pick_verifier_target_function,
    make_verifier_target_function,
)
from autoverify.util.loggers import hydra_logger
from autoverify.util.smac import costs_per_inst_from_rh
from autoverify.util.verifiers import verifier_from_name
from autoverify.verifier.verifier import CompleteVerifier, Verifier


class Hydra:
    # pick/tune, hydra_iter, smac_iter
    _SMAC_RUN_FMT: str = "iter_{}_{}_{}"

    @property
    def _instances(self) -> list[str]:
        return self._scenario.scenario_kwargs["instances"]

    def __init__(
        self,
        scenario: HydraScenario,
        *,
        iterations: int = 3,
        smac_per_iter: int = 2,
        incs_per_iter: int = 1,
        stop_early: bool = False,
        output_path: Path = Path("./"),
    ):
        self._scenario = scenario
        self._iterations = iterations

        if incs_per_iter > smac_per_iter:
            raise ValueError("incs_per_iter should be <= to smac_per_iter")

        self._smac_per_iter = smac_per_iter
        self._incs_per_iter = incs_per_iter
        self._stop_early = stop_early
        self._output_path = output_path

    def optimize(self) -> Portfolio:
        """_summary_."""
        self._init_dirs()
        self._init_hydra_run()

        portfolio = Portfolio()

        for self._iter in range(self._iterations):
            hydra_logger.info(f"Starting Hydra iteration {self._iter}")

            incumbents = self._do_smac_runs()
            self._update_portfolio(portfolio, incumbents)

        return portfolio

    def _init_dirs(self):
        self._output_dir = (
            self._output_path
            / "hydra_out"
            / str(datetime.datetime.today().replace(microsecond=0))
        )

        self._smac_dir = self._output_dir / "smac_runs"

    def _init_hydra_run(self):
        self._inst_costs: DefaultDict[str, float] = defaultdict(
            lambda: float("inf")
        )
        self._iter_costs: list[float] = []

    def _update_costs(self, costs: list[dict[str, list[float]]]):
        for cost_dict in costs:
            for inst, cost in cost_dict.items():
                self._inst_costs[inst] = min(self._inst_costs[inst], min(cost))

    def _update_portfolio(self, portfolio: Portfolio, incumbents: Incumbents):
        best_incs = incumbents.get_best_n(
            self._instances, self._incs_per_iter, remove_duplicates=True
        )

        costs: list[dict[str, list[float]]] = []

        for inc in best_incs:
            portfolio.add(inc.tuned_verifier)
            costs.append(costs_per_inst_from_rh(inc.runhistory, inc.config))

        self._update_costs(costs)
        # TODO: RESOURCE AWARE.

    def _get_pick_tune_time(self) -> tuple[float, float]:
        alpha = self._scenario.alpha
        walltime = self._scenario.scenario_kwargs["walltime_limit"]

        return walltime * alpha, walltime * (1 - alpha)

    def _pick_verifier(
        self, pick_time: float, scenario: Scenario
    ) -> type[Verifier]:
        if pick_time <= 0:
            random_verifier = random.choice(self._scenario.get_verifiers())
            return verifier_from_name(random_verifier)

        target_function = self._get_pick_tf()
        smac = AlgorithmConfigurationFacade(
            scenario,
            target_function,
            overwrite=True,
        )
        inc = smac.optimize()

        assert not isinstance(inc, list)  # please type-checkers, no m.o. anyway

        verifier = str(inc["verifier"])
        hydra_logger.info(f"Picked verifier: {verifier}")

        return verifier_from_name(verifier)

    def _tune_verifier(
        self,
        tune_time: float,
        verifier: type[CompleteVerifier],
        scenario: Scenario,
    ) -> Incumbent:
        if tune_time <= 0:
            return Incumbent((verifier, None))

        target_function = self._get_tune_tf(verifier)
        smac = AlgorithmConfigurationFacade(
            scenario,
            target_function,
            overwrite=True,
        )
        inc = smac.optimize()

        hydra_logger.info(f"Tuned verifier {verifier.name}")

        return Incumbent((verifier, inc), smac.runhistory)

    def _do_smac_runs(self) -> Incumbents:
        incumbents: Incumbents = Incumbents()
        pick_time, tune_time = self._get_pick_tune_time()

        for smac_iter in range(self._smac_per_iter):
            hydra_logger.info(f"Starting SMAC run {smac_iter}")

            verifier = self._pick_verifier(
                pick_time,
                self._scenario.as_smac_pick_scenario(
                    pick_time,
                    output_dir=self._output_dir
                    / self._SMAC_RUN_FMT.format("pick", self._iter, smac_iter),
                ),
            )

            # HACK: Should ideally not need this to please type checkers
            assert issubclass(verifier, CompleteVerifier)

            incumbent = self._tune_verifier(
                tune_time,
                verifier,
                self._scenario.as_smac_tune_scenario(
                    verifier.config_space,
                    tune_time,
                    output_dir=self._output_dir
                    / self._SMAC_RUN_FMT.format("tune", self._iter, smac_iter),
                ),
            )

            incumbents.append(incumbent)

        return incumbents

    def _hydra_tf(self, compare_tf: SmacTargetFunction) -> SmacTargetFunction:
        def tf(config: Configuration, instance: str, seed: int = 0) -> float:
            """_summary_."""
            config_cost = compare_tf(config, instance, seed)
            portfolio_cost = self._inst_costs[instance]

            return float(min(config_cost, portfolio_cost))

        return tf

    def _get_pick_tf(self) -> SmacTargetFunction:
        pick_tf = make_pick_verifier_target_function()

        if self._iter == 0:
            return pick_tf
        else:
            return self._hydra_tf(pick_tf)

    def _get_tune_tf(self, verifier: type[Verifier]) -> SmacTargetFunction:
        assert issubclass(verifier, CompleteVerifier)
        tune_tf = make_verifier_target_function(verifier)

        if self._iter == 0:
            return tune_tf
        else:
            return self._hydra_tf(tune_tf)
