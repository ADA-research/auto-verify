"""_summary_."""
import copy
import random
import sys

from ConfigSpace import Categorical, Configuration, ConfigurationSpace
from smac import AlgorithmConfigurationFacade, RunHistory, Scenario

from autoverify.util.cost_dict import (
    get_best_config_per_instance,
    merge_cost_dicts,
)
from autoverify.util.loggers import hydra_logger
from autoverify.util.smac import costs_from_runhistory
from autoverify.util.target_function import get_pick_tf, get_verifier_tf
from autoverify.verifier.verifier import Verifier

from ...types import ConfiguredVerifier, CostDict
from ..portfolio import Portfolio
from ..portfolio_scenario import PortfolioScenario


class Hydra:
    """_summary_."""

    def __init__(self, alpha: float = 0.5):
        if not 0 <= alpha <= 1:
            raise ValueError(f"Alpha should be in [0.0, 1.0], got {alpha}")

        self._tune_budget = 1 - alpha
        self._pick_budget = alpha

    def create_portfolio(self, pf_scenario: PortfolioScenario) -> Portfolio:
        portfolio = Portfolio()

        for i in range(pf_scenario.n_iters):
            hydra_logger.info(f"Starting Hydra iteration {i}")

            # initial_config = self._initial_config_provider(None, self._costs)
            new_configs, costs = self._configurator(pf_scenario)
            self._portfolio_updater(portfolio, new_configs, costs)

        return copy.deepcopy(portfolio)

    def _portfolio_updater(
        self,
        portfolio: Portfolio,
        configs: Configuration | list[Configuration],
        costs: CostDict,
    ):
        """
        - beste configs pakken
        - in de PF doen
        - kosten pf bijhouden
        """
        best = get_best_config_per_instance(costs)

        # for inst, cfg in best.items():
        #     cv = ConfiguredVerifier.from_verifier_config(cfg, (-1, -1))

        # portfolio.add()

    def _update_costs_from_runhistory(
        self,
        rh: RunHistory,
        curr_costs: CostDict,
        *,
        config_key: Configuration | None = None,
    ) -> CostDict:
        new_costs = costs_from_runhistory(rh)
        merged_costs = merge_cost_dicts(curr_costs, new_costs)
        # best_configs = get_best_config_per_instance(new_costs)

        # TODO: HIERZO:
        """
        - Merged implementatie dubbel checken: Prima vgm
        - Portfolio updaten op basis van de kosten
        - Maar geen configs weghalen?
        - Kosten van PF bijhouden in PF object?

        - Bekijk de gemiddelde performance van elke config uit deze smac run op
        elke instance, en voeg de beste daarvan toe aan de PF.
        - Update de PF performance door de beste cost per instance te pakken

        - Na iteratie 0 moet de tf -> hydra_tf worden
        - hydra_tf: Pak de laagste gecache waarde
        """
        # for k, v in merged_costs.items():
        #     print(k)
        #     print(v)
        #     print("...............................")

        return merged_costs

    def _configurator(
        self,
        pf_scenario: PortfolioScenario,
        *,
        initial_config: Configuration | None = None,
    ) -> tuple[Configuration | list[Configuration], CostDict]:
        new_configs: list[Configuration] = []
        all_costs: CostDict = {}

        for _ in range(pf_scenario.configs_per_iter):
            # TODO: Enable
            # if self._pick_budget > 0:
            #     picked_verifier, rh = self._pick_verifier(pf_scenario)
            #     all_costs = self._update_costs_from_runhistory(rh, all_costs)
            # else:
            #     pass
            picked_verifier = random.choice(pf_scenario.verifiers)

            hydra_logger.info(f"Picked {picked_verifier.name}")

            if self._tune_budget > 0:
                hydra_logger.info(f"Tuning {picked_verifier.name}")
                new_config, rh = self._tune_verifier(
                    picked_verifier, pf_scenario
                )
                # all_costs = self._update_costs_from_runhistory(rh, all_costs)
            else:
                new_config = picked_verifier.default_config

            hydra_logger.info(f"Tuned {picked_verifier.name}")
            hydra_logger.info(f"Got config: \n{new_config}")

            new_configs.append(new_config)

        return new_configs, all_costs

    def _pick_verifier(
        self, pf_scenario: PortfolioScenario
    ) -> tuple[Verifier, RunHistory]:
        # Create an "index" param to map it to an instantiated class
        # since those cannot be used as an HP directly
        index_space = ConfigurationSpace(name="index")
        index_space.add_hyperparameter(
            Categorical("index", [i for i in range(len(pf_scenario.verifiers))])
        )

        walltime_limit = (
            pf_scenario.seconds_per_iter
            * self._pick_budget
            / pf_scenario.configs_per_iter
        )

        scenario = Scenario(
            index_space,
            walltime_limit=walltime_limit,
            n_trials=sys.maxsize,  # we use walltime_limit
            **pf_scenario.get_smac_scenario_kwargs(),
        )

        pick_tf = get_pick_tf(pf_scenario.verifiers)
        smac = AlgorithmConfigurationFacade(scenario, pick_tf, overwrite=True)
        inc = smac.optimize()

        # Not dealing with > 1 config
        assert isinstance(inc, Configuration)
        return pf_scenario.verifiers[inc["index"]], smac.runhistory

    def _tune_verifier(
        self, verifier: Verifier, pf_scenario: PortfolioScenario
    ) -> tuple[Configuration, RunHistory]:
        walltime_limit = (
            pf_scenario.seconds_per_iter
            * self._tune_budget
            / pf_scenario.configs_per_iter
        )

        scenario = Scenario(
            verifier.config_space,
            walltime_limit=walltime_limit,
            n_trials=sys.maxsize,  # we use walltime_limit
            **pf_scenario.get_smac_scenario_kwargs(),
        )

        tune_tf = get_verifier_tf(verifier)
        smac = AlgorithmConfigurationFacade(scenario, tune_tf, overwrite=True)
        inc = smac.optimize()

        # Not dealing with > 1 config
        assert isinstance(inc, Configuration)
        return inc, smac.runhistory

    # TODO:
    def _initial_config_provider(
        self, config_space: ConfigurationSpace, costs: CostDict
    ):
        pass

    def _get_hydra_tf(self):
        # TODO:
        pass
