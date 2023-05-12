from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from ConfigSpace import Configuration
from smac.runhistory.runhistory import RunHistory

from hydrasmac.hydra.types import CostDict


@dataclass
class Incumbent:
    config: Configuration
    runhistory: RunHistory
    cost_dict: CostDict

    def mean_cost(self) -> float:
        return float(np.nanmean(list(self.cost_dict.values())))


@dataclass
class Incumbents:
    incumbents: list[Incumbent] = field(default_factory=list)

    def __iter__(self):
        return self.incumbents.__iter__()

    def __len__(self):
        return self.incumbents.__len__()

    def add_new_incumbent(self, incumbent: Incumbent) -> bool:
        if self._is_config_in_incumbents(incumbent.config):
            return False

        self.append(incumbent)

        return True

    def append(self, incumbent: Incumbent):
        self.incumbents.append(incumbent)

    def get_best_n(self, n: int) -> Incumbents:
        self._sort()
        return Incumbents(self.incumbents[:n])

    def get_configs(self) -> list[Configuration]:
        return [incumbent.config for incumbent in self.incumbents]

    def _sort(self):
        self.incumbents.sort(key=lambda inc: inc.mean_cost())

    def _is_config_in_incumbents(self, config: Configuration) -> bool:
        return config in self.get_configs()
