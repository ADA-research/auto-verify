"""_summary_."""

import numpy as np
from ConfigSpace import Configuration

from autoverify.types import CostDict, Instance


def merge_cost_dicts(*cost_dicts: CostDict) -> CostDict:
    """Merge multiple cost dicts into one."""
    res_cd: CostDict = {}

    for cd in cost_dicts:
        for inst, cfg_cost in cd.items():
            if inst not in res_cd:
                res_cd[inst] = {}

            for cfg, costs in cfg_cost.items():
                if cfg not in res_cd[inst]:
                    res_cd[inst][cfg] = []

                res_cd[inst][cfg] += costs

    return res_cd


def get_best_config_per_instance(
    cost_dict: CostDict,
) -> dict[Instance, Configuration]:
    """Gets the best configuration for reach instance."""
    best_configs: dict[Instance, Configuration] = {}

    for instance, config_costs in cost_dict.items():
        min_avg = np.inf
        min_cfg: Configuration | None = None

        for config, costs in config_costs.items():
            avg = float(np.mean(costs))

            if avg < min_avg:
                min_avg = avg
                min_cfg = config

        if isinstance(min_cfg, Configuration):
            best_configs[instance] = min_cfg

    return best_configs
