"""_summary_."""
from collections.abc import Iterable, MutableMapping

import numpy as np
from ConfigSpace import Configuration
from smac import RunHistory
from smac.runhistory.enumerations import StatusType

from autoverify.util import add_to_average


class InstanceCost(MutableMapping[str, float]):
    """_summary_."""

    def __init__(self):
        """_summary_."""
        self.store: dict[str, float] = {}
        # Map that stores the amount of values in the average cost
        # Needed for updating the average
        self._val_counts: dict[str, int] = {}

    def update_cost(self, key: str, val: float, *, size: int = 1):
        """Update the average."""
        if key not in self.store:
            self.store[key] = val
            self._val_counts[key] = 1
            return

        size = self._val_counts[key]
        average = self.store[key]
        self.store[key] = add_to_average(average, val, size)
        self._val_counts[key] += 1

    def __getitem__(self, key) -> float:
        """_summary_."""
        return self.store[key]

    def __setitem__(self, key, value):
        """_summary_."""
        self.store[key] = value

    def __delitem__(self, key):
        """_summary_."""
        del self.store[key]

    def __iter__(self):
        """_summary_."""
        return iter(self.store)

    def __len__(self):
        """_summary_."""
        return len(self.store)

    def __repr__(self):
        """_summary_."""
        return repr(self.store)


# TODO: Type annotations for class functions
class CostMatrix(MutableMapping[Configuration, InstanceCost]):
    """_summary_."""

    def __init__(self, *, par: int = 10):
        """_summary_."""
        self.matrix: dict[Configuration, InstanceCost] = {}
        self._par = par

    def update_matrix(self, runhistory: RunHistory):
        """_summary_."""
        config_instance_costs: dict[Configuration, dict[str, list[float]]] = {}

        for trial_key, trial_value in runhistory.items():
            config = runhistory.get_config(trial_key.config_id)

            instance = trial_key.instance
            assert instance is not None

            if config not in config_instance_costs:
                config_instance_costs[config] = {}

            # not dealing with > 1 cost
            assert isinstance(trial_value.cost, float)

            cost = trial_value.cost
            if trial_value.status == StatusType.TIMEOUT:
                cost *= self._par
            # # NOTE: Is this fair?
            # elif trial_value.status == StatusType.CRASHED:
            #     cost *= self._par

            if instance not in config_instance_costs[config]:
                config_instance_costs[config][instance] = [cost]
            else:
                config_instance_costs[config][instance].append(cost)

            if config not in self.matrix:
                self.matrix[config] = InstanceCost()

        for config, instance_costs in config_instance_costs.items():
            for instance, costs in instance_costs.items():
                self.matrix[config].update_cost(
                    instance, float(np.mean(costs)), size=len(costs)
                )

    def vbs_cost(
        self,
        configs: Iterable[Configuration],
        instances: list[str],
    ) -> dict[str, float]:
        """_summary_."""
        vbs_cost: dict[str, float] = {inst: np.inf for inst in instances}

        for config in configs:
            if config not in self.matrix:
                raise RuntimeError(f"Config {config} not in matrix")

            for instance, cost in self.matrix[config].items():
                if instance not in vbs_cost.keys():
                    continue

                vbs_cost[instance] = min(vbs_cost[instance], cost)

        return vbs_cost

    def __getitem__(self, key) -> InstanceCost:
        """_summary_."""
        return self.matrix[key]

    def __setitem__(self, key, value):
        """_summary_."""
        self.matrix[key] = value

    def __delitem__(self, key):
        """_summary_."""
        del self.matrix[key]

    def __iter__(self):
        """_summary_."""
        return iter(self.matrix)

    def __len__(self):
        """_summary_."""
        return len(self.matrix)

    def __repr__(self):
        """_summary_."""
        return repr(self.matrix)
