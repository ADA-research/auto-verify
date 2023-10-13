"""_summary_."""
from collections.abc import Sequence
from pathlib import Path

from autoverify.portfolio.hydra.hydra import Hydra
from autoverify.portfolio.portfolio import PortfolioScenario
from autoverify.util.resource_strategy import ResourceStrategy
from autoverify.util.verification_instance import VerificationInstance


def tune_hydra_portfolio(
    instances: Sequence[VerificationInstance],
    verifiers: Sequence[str],
    resources: list[tuple[str, int, int]],
    alpha: float,
    length: int,
    sec_per_iter: int,
    output_dir: Path,
    portfolio_out: Path,
    *,
    configs_per_iter: int = 1,
    added_per_iter: int = 1,
    stop_early: bool = False,
    resource_strategy: ResourceStrategy = ResourceStrategy.Auto,
    vnn_compat_mode: bool = False,
    benchmark: str | None = None,
):
    """_summary_."""
    pf_scen = PortfolioScenario(
        verifiers,
        # TODO: Resources,
        resources,
        instances,
        length,
        sec_per_iter,
        configs_per_iter,
        alpha,
        added_per_iter,
        stop_early,
        resource_strategy,
        output_dir,
        vnn_compat_mode,
        benchmark,
    )

    hydra = Hydra(pf_scen)
    portfolio = hydra.tune_portfolio()
    portfolio.to_json(portfolio_out)
    print(portfolio.str_compact())
