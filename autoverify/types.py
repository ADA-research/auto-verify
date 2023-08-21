"""_summary_."""
# from dataclasses import dataclass, field
from typing import Callable

from ConfigSpace import Configuration

# TODO: This is dumb, just use normal types
Instance = str
Cost = float
Seed = int

TargetFunction = Callable[[Configuration, Instance, Seed], Cost]
#
# # str implies str(configuration)
CostDict = dict[Instance, dict[Configuration, list[Cost]]]
#
# # TODO: Update Configurator, InitialConfigProvider, PortfolioUpdater
# Configurator = Callable[
#     [ConfigurationSpace, list[Instance], float, Configuration],
#     Cost,
# ]
#
# InitialConfigProvider
# = Callable[[ConfigurationSpace, CostDict], Configuration]
#
# # TODO: args and ret types
# PortfolioUpdater = Callable[[None], None]
#
# # Number of CPUs and GPUs
# ResourceUsage = tuple[int, int]
#
#
#
# @dataclass(frozen=True, eq=True, repr=True)
# class ConfiguredVerifier:
#     verifier: str
#     configuration: Configuration
#     resources: ResourceUsage
#
#     attributes: dict[str, Any] = field(default_factory=lambda: {})
#
#     @classmethod
#     def from_verifier_config(
#         cls,
#         cfg: Configuration,
#         resources: ResourceUsage,
#         attrs: dict[str, Any] | None = None,
#     ):
#         if attrs is None:
#             attrs = {}
#
#         verifier_name = cfg.config_space.name
#         assert verifier_name is not None
#         return cls(verifier_name, cfg, resources, attrs)
