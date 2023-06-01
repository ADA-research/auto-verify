"""_summary_."""

from dataclasses import dataclass
from typing import Literal

from result import Result

VerificationResultString = Literal["SAT", "UNSAT", "TIMEOUT", "ERR"]


@dataclass
class CompleteVerificationData:
    """_summary_."""

    result: VerificationResultString
    took: float
    counter_example: str | None = None
    err: str = ""
    stdout: str = ""


CompleteVerificationResult = Result[
    CompleteVerificationData, CompleteVerificationData
]
