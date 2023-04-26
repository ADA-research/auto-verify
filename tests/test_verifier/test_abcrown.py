from pathlib import Path

import pytest
from result import Err, Ok

from autoverify.verifier import AbCrown

from .conftest import VerificationInstance

# from tests.util import run_av_cli


@pytest.fixture
def abcrown() -> AbCrown:
    return AbCrown()


@pytest.mark.nn_prop
def test_sat(abcrown: AbCrown, trivial_sat: VerificationInstance):
    result = abcrown.verify_property(trivial_sat.property, trivial_sat.network)

    assert isinstance(result, Ok)
    assert result.value.result == "SAT"


@pytest.mark.nn_prop
def test_unsat(abcrown: AbCrown, trivial_unsat: VerificationInstance):
    result = abcrown.verify_property(
        trivial_unsat.property, trivial_unsat.network
    )

    assert isinstance(result, Ok)
    assert result.value.result == "UNSAT"


@pytest.mark.nn_prop
def test_err(abcrown: AbCrown):
    result = abcrown.verify_property(Path(), Path())

    assert isinstance(result, Err)
