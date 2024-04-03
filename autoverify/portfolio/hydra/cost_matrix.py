"""_summary_."""

from collections.abc import Iterable, MutableMapping

import numpy as np
from ConfigSpace import Configuration
from smac import RunHistory
from smac.runhistory.enumerations import StatusType

from autoverify.util import add_to_average


class InstanceCost(MutableMapping[str, float]):
    """Mapping from instance to cost."""

    def __init__(self):
        """Creates a new. empty `InstanceCost`."""
        self.store: dict[str, float] = {}
        # Map that stores the amount of values in the average cost
        # Needed for updating the average
        self._val_counts: dict[str, int] = {}

    def update_cost(self, key: str, val: float):
        """Update the cost of the key and value.

        Arguments:
            key: The instance.
            val: The cost.
        """
        if key not in self.store:
            self.store[key] = val
            self._val_counts[key] = 1
            return

        size = self._val_counts[key]
        average = self.store[key]
        self.store[key] = add_to_average(average, val, size)
        self._val_counts[key] += 1

    def __getitem__(self, key) -> float:
        """Get the value at the key."""
        return self.store[key]

    def __setitem__(self, key, value):
        """Set the value at the key."""
        self.store[key] = value

    def __delitem__(self, key):
        """Delete the value at the key."""
        del self.store[key]

    def __iter__(self):
        """Iterate over all costs."""
        return iter(self.store)

    def __len__(self):
        """Get the number of instances."""
        return len(self.store)

    def __repr__(self):
        """Repr."""
        return repr(self.store)


class CostMatrix(MutableMapping[Configuration, InstanceCost]):
    """Cost matrix of average cost per instance per configuration."""

    def __init__(self, *, par: int = 10):
        """Create a new, empty `CostMatrix`."""
        self.matrix: dict[Configuration, InstanceCost] = {}
        self._par = par

    def update_matrix(self, runhistory: RunHistory):
        """Update the matrix with a `RunHistory`."""
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

            if instance not in config_instance_costs[config]:
                config_instance_costs[config][instance] = [cost]
            else:
                config_instance_costs[config][instance].append(cost)

            if config not in self.matrix:
                self.matrix[config] = InstanceCost()

        for config, instance_costs in config_instance_costs.items():
            for instance, costs in instance_costs.items():
                self.matrix[config].update_cost(instance, float(np.mean(costs)))

    def vbs_cost(
        self,
        configs: Iterable[Configuration],
        instances: list[str],
    ) -> dict[str, float]:
        """Get the virtual best solver cost.

        Arguments:
            configs: The configurations that will be considered.
            instances: The instances that will be considered.

        Returns:
            dict[str, float]: The vbs cost for each instance.
        """
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
        """Get the value at the key."""
        return self.matrix[key]

    def __setitem__(self, key, value):
        """Set the value at the key."""
        self.matrix[key] = value

    def __delitem__(self, key):
        """Delete the value at the key."""
        del self.matrix[key]

    def __iter__(self):
        """Iterate over the cost matrix."""
        return iter(self.matrix)

    def __len__(self):
        """Get the number of elements in the cost matrix."""
        return len(self.matrix)

    def __repr__(self):
        """Repr."""
        return repr(self.matrix)
