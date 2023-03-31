from typing import Literal

from result import Result

VerifierKind = Literal["Complete", "Incomplete"]

Satisfiable = Literal["SAT", "UNSAT"]
CounterExample = str | None  # TODO: counterexample type (not just `str`)

CompleteVerificationOutcome = tuple[Satisfiable, CounterExample]

# TODO: error type (not just `str`)
CompleteVerificationResult = Result[CompleteVerificationOutcome, str]
