"""_summary_."""

from dataclasses import dataclass
from typing import Literal

from result import Result


# TODO: Use the counterexample specification from vnncomp2022
@dataclass
class CompleteVerificationOutcome:
    """_summary_."""

    result: Literal["SAT", "UNSAT"]
    counter_example: tuple[str, str] | None


# TODO: error type (not just `str`)
CompleteVerificationResult = Result[CompleteVerificationOutcome, str]
