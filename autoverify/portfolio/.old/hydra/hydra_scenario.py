from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from ConfigSpace import Categorical, ConfigurationSpace, Float
from smac import Scenario

from autoverify.portfolio.portfolio import ConfiguredVerifier
from autoverify.verifier.verifier import CompleteVerifier

CpuSpec = int
GpuSpec = Literal[0, 1]


@dataclass
class ResourceSpec:
    """_summary_."""

    cpus: CpuSpec
    gpus: GpuSpec

    def __post_init__(self):
        if not (self.cpus > 0 or self.cpus == -1):
            raise ValueError(f"CPUs should be > 0 or == -1, got {self.cpus}")

        if self.gpus != 0 and self.gpus != 1:
            raise ValueError(f"GPUs should be 0 or 1, got {self.gpus}")


VerifierResources = list[tuple[type[CompleteVerifier], ResourceSpec]]


@dataclass
class HydraScenario:
    """TODO.

    Args:
        verifier_resources: TODO.
        alpha: The time spent on picking vs tuning.
    """

    verifier_resources: VerifierResources
    resources: tuple[int, int]
    scenario_kwargs: dict[str, Any]
    alpha: float = field(default=0.5, kw_only=True)

    def __post_init__(self):
        if not (0 <= self.alpha <= 1):
            raise ValueError(f"alpha should be in [0, 1], got {self.alpha}")

        self._resources_left = copy.copy(self.resources)

    def get_verifiers(self, remove_duplicates=True) -> list[str]:
        """_summary_."""
        names = [i[0]().name for i in self.verifier_resources]

        if remove_duplicates:
            names = list(set(names))

        return names

    def as_smac_pick_scenario(
        self,
        pick_time: float,
        *,
        output_dir: Path | None = None,
    ) -> Scenario:
        """_summary_."""
        config_space = ConfigurationSpace()
        config_space.add_hyperparameters(
            [
                Categorical("verifier", self.get_verifiers()),
            ]
        )

        # TODO: pick_time is now always walltime limit
        # there are scenarios where we might want it to be
        # cpu time limit or something else
        scenario_kwargs = copy.deepcopy(self.scenario_kwargs)
        scenario_kwargs["walltime_limit"] = pick_time
        scenario_kwargs["output_directory"] = output_dir
        scenario_kwargs["deterministic"] = False

        return Scenario(config_space, **scenario_kwargs)

    def as_smac_tune_scenario(
        self,
        config_space: ConfigurationSpace,
        tune_time: float,
        *,
        output_dir: Path | None = None,
    ) -> Scenario:
        scenario_kwargs = copy.deepcopy(self.scenario_kwargs)
        scenario_kwargs["walltime_limit"] = tune_time
        scenario_kwargs["output_directory"] = output_dir
        scenario_kwargs["deterministic"] = False

        return Scenario(config_space, **scenario_kwargs)

    def deplete_resources(self, cpu: int, gpu: int):
        """_summary_."""
        cpus_left, gpus_left = self.get_resources_left()

        if cpus_left < cpu:
            raise ValueError(
                f"Tried to deplete CPU by {cpu} but there is only"
                f"{cpus_left} left."
            )

        if gpus_left < gpu:
            raise ValueError(
                f"Tried to deplete GPU by {gpu} but there is only"
                f"{gpus_left} left."
            )

        self._resources_left = (
            self._resources_left[0] - cpu,
            self._resources_left[1] - gpu,
        )

    def get_resources_left(self) -> tuple[int, int]:
        """_summary."""
        return self._resources_left[0], self._resources_left[1]

    def get_possible_verifiers(self) -> VerifierResources:
        """_summary."""
        possible: VerifierResources = []
        cpus_left, gpus_left = self.get_resources_left()

        if cpus_left <= 0:
            return possible

        for verifier, resource_spec in self.verifier_resources:
            if resource_spec.cpus == -1:
                possible.append((verifier, resource_spec))
                continue

            if (
                resource_spec.gpus >= gpus_left
                and resource_spec.cpus >= cpus_left
            ):
                possible.append((verifier, resource_spec))

        return possible
