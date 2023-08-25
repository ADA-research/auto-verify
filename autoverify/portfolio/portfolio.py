"""_summary_."""
import datetime
import math
from collections.abc import Iterable, Mapping, MutableSet, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from ConfigSpace import Configuration

from autoverify.util.instances import verification_instances_to_smac_instances
from autoverify.util.resource_strategy import ResourceStrategy
from autoverify.util.smac import index_features
from autoverify.util.verification_instance import VerificationInstance


@dataclass(frozen=True, eq=True, repr=True)
class ConfiguredVerifier:
    """_summary_."""

    verifier: str
    configuration: Configuration


@dataclass
class PortfolioScenario:
    """_summary_."""

    verifiers: Sequence[str]
    resources: list[tuple[str, int, int]]
    instances: Sequence[VerificationInstance]
    length: int
    seconds_per_iter: float

    # Optional
    configs_per_iter: int = 2
    alpha: float = 0.5  # tune/pick split
    added_per_iter: int = 1
    stop_early = True
    resource_strategy = ResourceStrategy.Auto
    output_dir: Path | None = None
    verifier_kwargs: Mapping[str, dict[str, Any]] | None = None

    def __post_init__(self):
        """_summary_."""
        if self.added_per_iter > 1:
            raise ValueError(
                "Adding more than 1 config per iter not supported yet."
            )

        if not 0 <= self.alpha <= 1:
            raise ValueError(f"Alpha should be in [0.0, 1.0], got {self.alpha}")

        if self.output_dir is None:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            self.output_dir = Path(f"hydra_out/{formatted_time}")

        self.tune_budget = self.alpha
        self.pick_budget = 1 - self.alpha

        if self.added_per_iter > self.length:
            raise ValueError("Entries added per iter should be <= length")

        self.n_iters = math.ceil(self.length / self.added_per_iter)
        self._verify_resources()

    def _verify_resources(self):
        # Check for duplicates
        seen = set()
        for r in self.resources:
            if r[0] in seen:
                raise ValueError(f"Duplicate name '{r[0]}' in resources")

            seen.add(r[0])

        if self.resource_strategy == ResourceStrategy.Auto:
            for r in self.resources:
                if r[1] != 0:
                    raise ValueError(
                        "CPU resources should be 0 when using `Auto`"
                    )
        else:
            raise NotImplementedError(
                f"ResourceStrategy {self.resource_strategy} "
                f"is not implemented yet."
            )

    def get_smac_scenario_kwargs(self) -> dict[str, Any]:
        """_summary_."""
        assert self.output_dir is not None  # This is set in `__post_init__`
        self.output_dir.mkdir(parents=True, exist_ok=True)

        return {
            "instances": verification_instances_to_smac_instances(
                self.instances
            ),
            "instance_features": index_features(self.instances),
            "output_directory": self.output_dir,
        }

    def get_smac_instances(self) -> list[str]:
        """Get the instances of the scenario as SMAC instances."""
        return verification_instances_to_smac_instances(self.instances)


class Portfolio(MutableSet[ConfiguredVerifier]):
    """_summary_."""

    def __init__(self, *cvs: ConfiguredVerifier):
        """_summary_."""
        self._pf_set: set[ConfiguredVerifier] = set(cvs)
        self._costs: dict[str, float] = {}

    def __contains__(self, cv: object):
        """_summary_."""
        # cant type annotate the func arg or mypy gets mad
        assert isinstance(cv, ConfiguredVerifier)
        return cv in self._pf_set

    def __iter__(self):
        """_summary_."""
        return iter(self._pf_set)

    def __len__(self):
        """_summary_."""
        return len(self._pf_set)

    def __str__(self):
        """_summary_."""
        res = ""

        for cv in self:
            res += str(cv) + "\n"

        return res

    @property
    def configs(self) -> list[Configuration]:
        """_summary_."""
        configs = []

        for cv in self._pf_set:
            configs.append(cv.configuration)

        return configs

    def get_cost(self, instance: str):
        """_summary_."""
        return self._costs[instance]

    def get_costs(self, instances: Iterable[str]) -> dict[str, float]:
        """_summary_."""
        costs: dict[str, float] = {}

        for inst in instances:
            if inst in self._costs:
                costs[inst] = self._costs[inst]

        return costs

    def get_mean_cost(self) -> float:
        """_summary_."""
        return float(np.mean(list(self._costs.values())))

    def get_total_cost(self) -> float:
        """_summary_."""
        return float(np.sum(list(self._costs.values())))

    def update_costs(self, costs: Mapping[str, float]):
        """_summary_."""
        for instance, cost in costs.items():
            if instance not in self._costs:
                self._costs[instance] = cost
                continue

            self._costs[instance] = min(self._costs[instance], cost)

    def add(self, cv: ConfiguredVerifier):
        """_summary_."""
        if cv in self._pf_set:
            raise ValueError(f"{cv} is already in the portfolio")

        self._pf_set.add(cv)

    def discard(self, cv: ConfiguredVerifier):
        """_summary_."""
        if cv not in self._pf_set:
            raise ValueError(f"{cv} is not in the portfolio")

        self._pf_set.discard(cv)
