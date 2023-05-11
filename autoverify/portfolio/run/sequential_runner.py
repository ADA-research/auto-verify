"""_summary_."""


from typing import Type

from ConfigSpace import Configuration

from autoverify.portfolio.target_function import run_smac_instance
from autoverify.util.instances import VerificationInstance
from autoverify.verifier.verifier import CompleteVerifier


def run_sequential_portfolio(
    portfolio: list[tuple[Type[CompleteVerifier], Configuration]],
    instances: list[VerificationInstance],
):
    """Run a portfolio sequentially on a set of instances.

    This is a very naive function meant for quick experimenting, it will
    run a set of configurations on a set of instances one by one, meaning
    each config is ran on each instance, after which the results are accumulated
    and reported.

    Args:
        portfolio: TODO.
        instances: TODO.

    Returns:
        TODO.
    """
    for verifier, config in portfolio:
        for instance in instances:
            result, took_t = run_smac_instance(
                verifier, config, instance.as_smac_instance()
            )
            print(result, took_t)
            break
        break
