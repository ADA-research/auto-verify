from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import cast

import numpy as np
from ConfigSpace import Configuration
from smac import RunHistory

from autoverify.portfolio.portfolio import ConfiguredVerifier
from autoverify.verifier.verifier import CompleteVerifier


@dataclass
class Incumbent:
    """_summary_."""

    tuned_verifier: ConfiguredVerifier
    runhistory: RunHistory = RunHistory()

    def __post_init__(self):
        self.config = self.tuned_verifier[1]

    def to_hashable(self) -> str:
        """_summary_."""
        d: dict[str, str] = {}

        d["verifier"] = self.tuned_verifier[0]().name
        d["config"] = str(self.config)

        return json.dumps(d, sort_keys=True)

    def mean_cost(self, instances: list[str]) -> float:
        """_summary_."""
        return float(
            np.nanmean(list(self.mean_cost_per_instance(instances).values()))
        )

    def mean_cost_per_instance(self, instances: list[str]) -> dict[str, float]:
        instance_cost: dict[str, list[float]] = {k: [] for k in instances}

        for isb in self.runhistory.get_instance_seed_budget_keys(self.config):
            if isb.instance is None:
                continue

            if not instance_cost[isb.instance]:
                instance_cost[isb.instance] = []

            mean_cost = cast(
                float,
                self.runhistory.average_cost(
                    self.config, [isb], normalize=True
                ),
            )

            instance_cost[isb.instance].append(mean_cost)

        mean_instance_cost: dict[str, float] = {}

        for instance, costs in instance_cost.items():
            mean_instance_cost[instance] = (
                float(np.mean(costs)) if costs else np.nan
            )

        return mean_instance_cost


@dataclass
class Incumbents:
    """_summary_."""

    incumbents: list[Incumbent] = field(default_factory=list)

    def __post_init__(self):
        self._incs_seen = set()

    def __iter__(self):
        """_summary_."""
        return self.incumbents.__iter__()

    def __len__(self):
        """_summary_."""
        return self.incumbents.__len__()

    def __getitem__(self, *args, **kwargs):
        return self.incumbents.__getitem__(*args, **kwargs)

    def _track_inc(self, incumbent: Incumbent):
        name = incumbent.tuned_verifier[0].name
        config = incumbent.tuned_verifier[1]

        self._incs_seen.add((name, config))

    def append(self, incumbent: Incumbent):
        """_summary_."""
        self._track_inc(incumbent)
        self.incumbents.append(incumbent)

    def get_unique_incs(self) -> Incumbents:
        """_summary_."""
        unique_incs: list[Incumbent] = []
        seen: set[str] = set()

        for inc in self.incumbents:
            h_inc = inc.to_hashable()

            if h_inc not in seen:
                unique_incs.append(inc)
            else:
                seen.add(h_inc)

        return Incumbents(unique_incs)

    def get_best_n(
        self,
        instances: list[str],
        n: int,
        *,
        remove_duplicates: bool = True,
    ) -> Incumbents:
        incs_to_sort = (
            self.get_unique_incs() if remove_duplicates else self.incumbents
        )

        sorted_incs = sorted(
            incs_to_sort, key=lambda inc: inc.mean_cost(instances)
        )

        return Incumbents(sorted_incs[:n])
