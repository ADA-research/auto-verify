from dataclasses import dataclass
from typing import Literal

from result import Result


@dataclass
class CompleteVerificationOutcome:
    """_summary_."""

    result: Literal["SAT", "UNSAT"]
    counter_example: str | None  # TODO: counterexample type (not just `str`)


# TODO: error type (not just `str`)
CompleteVerificationResult = Result[CompleteVerificationOutcome, str]
