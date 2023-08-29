"""_summary_."""
from typing import TypeVar

from autoverify.portfolio.portfolio import Portfolio
from autoverify.util.instances import VerificationDataResult
from autoverify.util.verification_instance import VerificationInstance

_T = TypeVar("_T", VerificationInstance, str)


class PortfolioRunner:
    """_summary_."""

    def __init__(self, portfolio: Portfolio):
        """_summary_."""
        self._portfolio = portfolio
        # TODO: santiy check and fix all resources

    def verify_instances(
        self, instances: list[_T]
    ) -> dict[_T, VerificationDataResult]:
        """_summary_."""
        # TODO:
        #     - launch all verifiers in parallel
        #     - as soon as one finds a result:
        #       - save result
        #       - stop all verifiers
        #     - go to next instance
        results: dict[_T, VerificationDataResult] = {}

        return results
