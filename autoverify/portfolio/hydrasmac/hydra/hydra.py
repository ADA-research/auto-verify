"""_summary."""
from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import DefaultDict, cast

import numpy as np
from ConfigSpace import Configuration
from smac import AlgorithmConfigurationFacade
from smac.runhistory.runhistory import RunHistory
from smac.scenario import Scenario

from autoverify.portfolio.hydrasmac.hydra.incumbents import (
    Incumbent,
    Incumbents,
)
from autoverify.portfolio.hydrasmac.hydra.types import CostDict, TargetFunction
from autoverify.portfolio.hydrasmac.util.scenario_util import (
    set_scenario_output_dir,
)
from autoverify.util.loggers import verification_logger


class Hydra:
    """_summary_."""

    def __init__(
        self,
        scenario: Scenario,
        target_function: TargetFunction,
        *,
        hydra_iterations: int = 3,
        smac_runs_per_iter: int = 2,
        incumbents_added_per_iter: int = 1,
        stop_early: bool = True,
        output_dir_path: Path = Path("./"),
        output_dir_name: str | None = None,
    ):
        """Class to use `Hydra` for constructing a portfolio of configurations.

        Args:
            scenario: Scenario
                The scenario object, holding all environmental information.
            target_function: Callable
                Cost function to be minimized
            hydra_iterations: int
                The number of Hydra iterations
            smac_runs_per_iter: int
                The number of SMAC runs that are performed at each Hydra
                iteration.
            incumbents_added_per_iter: int
                The number of incumbents that are added to the portfolio after
                each Hydra iteration. This value cannot be higher than the
                number of SMAC runs that are started each iteration.
            stop_early: bool
                Determines if the Hydra procedure is stopped before the maximum
                number of iterations is reached, by checking if portfolio
                performance has not improved compared to the previous iteration
                or if a configuration that is already present in the portfolio
                is returned by a SMAC run.
            output_dir_path: Path
                The path where the `hydra_output` directory will be created
            output_dir_name: str
                The name given to the output folder of the run
        """
        self._scenario = scenario
        self._target_function = target_function
        self._hydra_iterations = hydra_iterations

        if incumbents_added_per_iter > smac_runs_per_iter:
            raise ValueError(
                "The number of incumbents added per iteration cannot be larger "
                "than the number of SMAC runs per iteration"
            )

        self._smac_runs_per_iter = smac_runs_per_iter
        self._incumbents_added_per_iter = incumbents_added_per_iter
        self._stop_early = stop_early

        self._instances = self._scenario.instances
        self._instance_features = self._scenario.instance_features

        self._top_output_dir = Path(
            output_dir_path
            / f"hydra_output/{output_dir_name or datetime.now()}"
        )

        self._smac_run_output_dir = self._top_output_dir / "smac_runs"
        self._valdation_run_output_dir = (
            self._top_output_dir / "validation_runs"
        )

        self._has_duplicates_this_iter = False

        # Hydra iter, SMAC iter
        self._smac_run_name = "iter_{}_{}"

        # instance, config portfolio index
        self._validation_run_name = "valid_{}_{}"

    def optimize(self) -> list[Configuration]:
        """Constructs a new portfolio of configurations.

        Returns
            list[Configuration]: The portfolio of configurations.
        """
        self.portfolio: list[Configuration] = []
        self._cost_per_instance: DefaultDict[str, float] = defaultdict(
            lambda: math.inf
        )
        self._cost_each_iter: list[float] = []
        self._hydra_iter: int = 0

        for self._hydra_iter in range(self._hydra_iterations):
            verification_logger.info(
                f"Starting Hydra iteration {self._hydra_iter}"
            )

            incumbents = self._do_smac_runs()
            self._update_portfolio(incumbents)

            if self._hydra_iter > 0 and self._should_stop_early():
                verification_logger.info(
                    f"Performance stagnated after iteration {self._hydra_iter},"
                    " terminating..."
                )
                break

            verification_logger.info(
                f"Cost after iteration {self._hydra_iter} "
                f"is {self._cost_each_iter[self._hydra_iter]}"
            )

        print(f"{'Iteration':<10} {'Cost':<25}")
        print("=" * 35)

        for i, cost in enumerate(self._cost_each_iter):
            print(f"{i:<10} {cost:<20}")

        print("=" * 35)

        return self.portfolio

    def validate(
        self,
        portfolio: list[Configuration],
        instances: list[str],
        instance_features: dict[str, list[float]],
    ) -> CostDict:
        """Validate the performance of a portfolio on the validation instances.

        Args:
            portfolio: list[Configuration]
                The list of configurations to be validated on the test instances
            instances: list[str]
                The names of the instances to validate, e.g. name of a dataset
            instance_features: dict[str, list[float]]
                The (meta) features of each instance, e.g. average

        Returns:
            dict[str, float]: The smallest validated cost per instance.
        """
        # HACK: Currently there is no way to validate per instance in SMAC3 v2,
        # see https://github.com/automl/SMAC3/issues/909
        # TODO: Make this respect scenario parameters like time limits
        cost_per_instance: CostDict = {}

        for i, config in enumerate(portfolio):
            for instance in instances:
                run_name = self._validation_run_name.format(instance, i)
                scenario = Scenario(
                    config,
                    instances=[instance],
                    instance_features={instance: instance_features[instance]},
                )

                scenario = set_scenario_output_dir(
                    scenario, self._valdation_run_output_dir, run_name
                )

                cost = self._target_function(config, instance, 0)

                if instance not in cost_per_instance:
                    cost_per_instance[instance] = cost
                else:
                    cost_per_instance[instance] = min(
                        cost_per_instance[instance], cost
                    )

        return cost_per_instance

    # TODO: Fix docstring
    def _hydra_target_function(
        self, config: Configuration, instance: str, seed: int = 0
    ) -> float:
        """Defines a new metric to evaluate target function runs, by returning.

        the performance of the portfolio in cases where the portfolio
        outperforms the current configuration.
        """
        config_cost = self._target_function(config, instance, seed)
        portfolio_cost = self._cost_per_instance[instance]

        print(
            f"Instance {instance:<40}"
            f"Config cost {config_cost:<40}"
            f"Portfolio cost: {portfolio_cost:<40}"
        )

        return float(min(config_cost, portfolio_cost))

    def _should_stop_early(self) -> bool:
        """Check if the portfolio performance has stagnated."""
        if not self._stop_early:
            return False
        elif self._has_duplicates_this_iter:
            return True
        elif self._portfolio_cost >= self._cost_each_iter[self._hydra_iter - 1]:
            return True
        else:
            return False

    # TODO: (UNSURE) Now looping over instances without considering different
    #       seeds and budgets, could lead to unfair comparisons?
    def _average_cost_per_instance(
        self, config: Configuration, runhistory: RunHistory
    ) -> CostDict:
        instance_costs: dict[str, list[float]] = {
            k: [] for k in self._instances  # type: ignore
        }

        for isb in runhistory.get_instance_seed_budget_keys(config):
            if isb.instance is None:
                continue

            avg_cost = runhistory.average_cost(config, [isb], normalize=True)
            avg_cost = cast(float, avg_cost)  # no m.o. support atm

            instance_costs[isb.instance].append(avg_cost)

        mean_instance_costs: CostDict = {}

        for instance, costs in instance_costs.items():
            mean_instance_costs[instance] = (
                float(np.mean(costs)) if costs else np.nan
            )

            print(
                f"Instance: {instance:<30}"
                f"Cost {mean_instance_costs[instance]:<30}"
            )

        return mean_instance_costs

    # TODO: Fix docstring
    def _do_smac_runs(self) -> Incumbents:
        """Starts the SMAC runs and returns the incumbent configurations.

        corresponding runhistories and incumbent cost found by the runs.
        """
        incumbents = Incumbents()

        if self._hydra_iter == 0:
            target_function = self._target_function
        else:
            target_function = self._hydra_target_function

        for smac_iter in range(self._smac_runs_per_iter):
            verification_logger.info(f"Starting SMAC run {smac_iter}")

            run_name = self._smac_run_name.format(self._hydra_iter, smac_iter)
            scenario = set_scenario_output_dir(
                self._scenario, self._top_output_dir, run_name
            )

            smac = AlgorithmConfigurationFacade(
                scenario=scenario,
                target_function=target_function,
            )
            incumbent_config = smac.optimize()
            runhistory = smac.runhistory

            was_added = incumbents.add_new_incumbent(
                Incumbent(
                    incumbent_config,
                    runhistory,
                    self._average_cost_per_instance(
                        incumbent_config, runhistory
                    ),
                )
            )

            if not was_added:
                verification_logger.info(
                    f"Incumbent in SMAC iter {smac_iter} not added because"
                    " it was already present in the incumbents"
                )

        return incumbents

    def _update_portfolio_cost(self):
        """Updates the mean cost of the portfolio."""
        self._portfolio_cost = float(
            np.mean(list(self._cost_per_instance.values()))
        )
        self._cost_each_iter.append(self._portfolio_cost)

    # TODO: Fix docstring
    def _update_cost_per_instance(self, incumbents: Incumbents):
        """Update the cost per instance based on the new incumbents and.

        evaluated instances. Unevaluated instances get the mean instead.
        """
        min_costs = []

        for inc in incumbents:
            for instance, cost in inc.cost_dict.items():
                min_cost = min(self._cost_per_instance[instance], cost)
                self._cost_per_instance[instance] = min_cost

                if min_cost != math.inf:
                    min_costs.append(min_cost)

        # Need to initialize unevaluated instances in the first iteration
        if self._hydra_iter == 0:
            mean_cost = np.mean(min_costs)

            for instance, cost in self._cost_per_instance.items():
                if cost == math.inf:
                    self._cost_per_instance[instance] = float(mean_cost)

    # TODO: Fix docstring
    def _add_new_incumbents_to_portfolio(self, incumbents: Incumbents):
        """Extends the portfolio with new configs.The new cost of the portfolio.

        is also computed.
        """
        for inc in incumbents:
            self.portfolio.append(inc.config)

        self._update_cost_per_instance(incumbents)
        self._update_portfolio_cost()

    def _has_duplicates(self, incumbents: Incumbents) -> bool:
        for config in incumbents.get_configs():
            if config in self.portfolio:
                return True

        return False

    # TODO: Fix docstring
    def _update_portfolio(
        self,
        incumbents: Incumbents,
    ):
        """Update the portfolio with the incumbents and compute the new.

        cost of the portfolio.
        """
        incumbents = incumbents.get_best_n(self._incumbents_added_per_iter)
        self._has_duplicates_this_iter = self._has_duplicates(incumbents)

        # TODO: Not all incs have to be duplicates
        if self._has_duplicates_this_iter:
            verification_logger.info(
                "SMAC runs returned configurations already present in the "
                f"portfolio in iteration {self._hydra_iter}"
            )

            self._has_duplicates_this_iter = True
            self._cost_each_iter.append(
                self._cost_each_iter[self._hydra_iter - 1]
            )

            return

        self._add_new_incumbents_to_portfolio(incumbents)
