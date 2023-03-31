"""Types to be used with verifiers."""

from typing import Literal

from result import Result

VerifierKind = Literal["complete", "incomplete"]

Satisfiable = Literal["SAT", "UNSAT"]
CounterExample = str | None  # TODO: counterexample type (not just `str`)

CompleteVerificationOutcome = tuple[Satisfiable, CounterExample]
# TODO: error type (not just `str`)
CompleteVerificationResult = Result[CompleteVerificationOutcome, str]
