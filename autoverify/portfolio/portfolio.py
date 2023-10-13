"""Parallel portfolio."""
from __future__ import annotations

import datetime
import json
import math
from collections.abc import Iterable, Mapping, MutableSet, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from ConfigSpace import Configuration, ConfigurationSpace

from autoverify.util.instances import verification_instances_to_smac_instances
from autoverify.util.proc import cpu_count
from autoverify.util.resource_strategy import ResourceStrategy
from autoverify.util.smac import index_features
from autoverify.util.verification_instance import VerificationInstance
from autoverify.util.verifiers import get_verifier_configspace


@dataclass(frozen=True, eq=True, repr=True)
class ConfiguredVerifier:
    """Class representing an interal configured verifier.

    Attributes:
        verifier: Name of the verifier.
        configuration: Its configuration.
        resources: Number of cores and GPUs.
    """

    verifier: str
    configuration: Configuration
    resources: tuple[int, int] | None = None


@dataclass
class PortfolioScenario:
    """Scenario for constructing a parallel portfolio.

    Attributes:
        verifiers: The name of the verifiers to consider.
        resources: How many cores and GPUs the verifiers need.
        instances: The instances on which the PF is constructed.
        length: The max length of the PF.
        seconds_per_iter: Number of seconds for each Hydra iteration.
        configs_per_iter: Number of configs each iteration.
        alpha: Tune/Pick time split.
        added_per_iter: Entries added to the PF per iter.
        stop_early: Stop procedure if some early stop conditions are met.
        resource_strategy: Strat to divide the resources.
        output_dir: Dir where logs are stored.
        vnn_compat_mode: Use vnn compatability for some verifiers.
        benchmark: VNNCOMP benchmark if vnn_compat_mode is `True`.
        verifier_kwargs: Kwargs passed to verifiers.
        uses_simplified_network: If the network uses the dnnv simplified nets.
    """

    verifiers: Sequence[str]
    resources: list[tuple[str, int, int]]
    instances: Sequence[VerificationInstance]
    length: int  # TODO: Rename to max_length?
    seconds_per_iter: float

    # Optional
    configs_per_iter: int = 1
    alpha: float = 0.5  # tune/pick split
    added_per_iter: int = 1
    stop_early: bool = True
    resource_strategy: ResourceStrategy = ResourceStrategy.Auto
    output_dir: Path | None = None
    vnn_compat_mode: bool = False
    benchmark: str | None = None
    verifier_kwargs: dict[str, dict[str, Any]] | None = None
    uses_simplified_network: Iterable[str] | None = None

    def __post_init__(self):
        """Validate the PF scenario."""
        if self.added_per_iter > 1 or self.configs_per_iter > 1:
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

        if self.vnn_compat_mode:
            if not self.benchmark:
                raise ValueError("Use a benchmark name if vnn_compat_mode=True")

        if self.vnn_compat_mode and self.verifier_kwargs:
            raise ValueError(
                "Cannot use vnn_compat_mode and "
                "verifier_kwargs at the same time."
            )

        self.n_iters = math.ceil(self.length / self.added_per_iter)
        self._verify_resources()

    def _verify_resources(self):
        # Check for duplicates
        seen = set()
        for r in self.resources:
            if r[0] in seen:
                raise ValueError(f"Duplicate name '{r[0]}' in resources")

            if r[0] not in self.verifiers:
                raise ValueError(f"{r[0]} in resources but not in verifiers.")

            seen.add(r[0])

        for v in self.verifiers:
            if v not in seen:
                raise ValueError(
                    f"Verifier '{v}' in verifiers but not in resources."
                )

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
        """Return the SMAC scenario kwargs as a dict.

        Returns:
            dict[str, Any]: The SMAC scenario as a dict.
        """
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
        """Get the instances of the scenario as SMAC instances.

        Returns:
            list[str]: The SMAC instances.
        """
        return verification_instances_to_smac_instances(self.instances)


class Portfolio(MutableSet[ConfiguredVerifier]):
    """Portfolio of ConfiguredVerifiers."""

    def __init__(self, *cvs: ConfiguredVerifier):
        """Initialize a new PF with the passed verifiers."""
        self._pf_set: set[ConfiguredVerifier] = set(cvs)
        self._costs: dict[str, float] = {}

    def __contains__(self, cv: object):
        """Check if a CV is in the PF."""
        # cant type annotate the func arg or mypy gets mad
        assert isinstance(cv, ConfiguredVerifier)
        return cv in self._pf_set

    def __iter__(self):
        """Iterate the contents of the PF."""
        return iter(self._pf_set)

    def __len__(self):
        """Number of CVs in the PF."""
        return len(self._pf_set)

    def __str__(self):
        """String representation of the PF."""
        res = ""

        for cv in self:
            res += str(cv) + "\n"

        return res

    def get_set(self):
        """Get the underlying set."""
        return self._pf_set

    @property
    def configs(self) -> list[Configuration]:
        """All the configurations in the PF."""
        configs = []

        for cv in self._pf_set:
            configs.append(cv.configuration)

        return configs

    def get_cost(self, instance: str):
        """Get the currently known costs of an instance."""
        return self._costs[instance]

    def get_costs(self, instances: Iterable[str]) -> dict[str, float]:
        """Get costs of more than one instance."""
        costs: dict[str, float] = {}

        for inst in instances:
            if inst in self._costs:
                costs[inst] = self._costs[inst]

        return costs

    def get_all_costs(self) -> dict[str, float]:
        """All the recorded costs."""
        return self._costs

    def get_mean_cost(self) -> float:
        """Get the mean cost."""
        return float(np.mean(list(self._costs.values())))

    def get_median_cost(self) -> float:
        """Get the median cost."""
        return float(np.median(list(self._costs.values())))

    def get_total_cost(self) -> float:
        """Get the total cost."""
        return float(np.sum(list(self._costs.values())))

    def update_costs(self, costs: Mapping[str, float]):
        """Upate the costs based on the new costs mapping."""
        for instance, cost in costs.items():
            if instance not in self._costs:
                self._costs[instance] = cost
                continue

            self._costs[instance] = min(self._costs[instance], cost)

    def add(self, cv: ConfiguredVerifier):
        """Add a CV to the PF, no duplicates allowed."""
        if cv in self._pf_set:
            raise ValueError(f"{cv} is already in the portfolio")

        self._pf_set.add(cv)

    def discard(self, cv: ConfiguredVerifier):
        """Remove a CV from the PF."""
        if cv not in self._pf_set:
            raise ValueError(f"{cv} is not in the portfolio")

        self._pf_set.discard(cv)

    def reallocate_resources(
        self, strategy: ResourceStrategy = ResourceStrategy.Auto
    ):
        """Realloacte based on current contents and given strategy."""
        if strategy != ResourceStrategy.Auto:
            raise NotImplementedError(
                "Given `ResourceStrategy` is not supported yet."
            )

        # NOTE: Should put this alloc stuff in a function
        n_cores = cpu_count()
        cores_per = n_cores // len(self)
        cores_remainder = n_cores % len(self)

        for cv in self:
            verifier = cv.verifier
            resources = cv.resources
            config = cv.configuration

            extra_core = 0
            if cores_remainder > 0:
                extra_core = 1
                cores_remainder -= 1

            new_resources = (
                (cores_per + extra_core, resources[1]) if resources else None
            )

            self.discard(cv)
            self.add(ConfiguredVerifier(verifier, config, new_resources))

    def to_json(self, out_json_path: Path):
        """Write the portfolio in JSON format to the specified path."""
        json_list: list[dict[str, Any]] = []

        for cv in self._pf_set:
            cfg_dict = dict(cv.configuration)
            to_write = {
                "verifier": cv.verifier,
                "configuration": cfg_dict,
                "resources": cv.resources,
            }
            json_list.append(to_write)

        with open(out_json_path, "w") as f:
            json.dump(json_list, f, indent=4, default=str)

    @classmethod
    def from_json(
        cls,
        json_file: Path,
        config_space_map: Mapping[str, ConfigurationSpace] | None = None,
    ) -> Portfolio:
        """Instantiate a new Portfolio class from a JSON file."""
        with open(json_file.expanduser().resolve()) as f:
            pf_json = json.load(f)

        pf = Portfolio()

        for cv in pf_json:
            if config_space_map is None:
                cfg_space = get_verifier_configspace(cv["verifier"])
            else:
                cfg_space = config_space_map[cv["verifier"]]

            cv["configuration"] = Configuration(cfg_space, cv["configuration"])

            if cv["resources"]:
                cv["resources"] = tuple(cv["resources"])

            pf.add(ConfiguredVerifier(**cv))

        return pf

    def str_compact(self) -> str:
        """Get the portfolio in string form in a compact way."""
        cvs: list[str] = []

        for cv in self:
            cvs.append(
                "\t".join(
                    [
                        str(cv.verifier),
                        str(hash(cv.configuration)),
                        str(cv.resources),
                    ]
                )
            )

        return "\n".join(cvs)

    def dump_costs(self):
        """Print the costs for each instance."""
        for instance, cost in self._costs.items():
            print(instance, cost)
