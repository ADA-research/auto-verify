import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from autoverify.util.smac import index_features
from autoverify.verifier.verifier import Verifier


@dataclass
class PortfolioScenario:
    verifiers: list[Verifier]
    instances: list[str]
    length: int
    seconds_per_iter: float

    # optional kwargs
    configs_per_iter: int = 2
    added_per_iter: int = 1
    output_dir: Path = Path("./hydra_out")

    def __post_init__(self):
        if self.added_per_iter > self.length:
            raise ValueError("Entries added per iter should be <= length")

        # FIXME: Strange to do list(set()) on class instances
        # self.verifiers = list(set(self.verifiers))  # remove duplicates
        self.n_iters = math.ceil(self.length / self.added_per_iter)

        self._setup_configspaces()

    def _setup_configspaces(self):
        self.configspaces = {v.name: v.config_space for v in self.verifiers}

    def get_smac_scenario_kwargs(self) -> dict[str, Any]:
        """_summary_."""

        return {
            "instances": self.instances,
            "instance_features": index_features(self.instances),
            "output_directory": self.output_dir,
        }
