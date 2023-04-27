import os
from pathlib import Path

import pytest
from result import Err, Ok

from autoverify.util.env import get_file_path
from autoverify.verifier import AbCrown

from .conftest import VerificationInstance


@pytest.fixture(autouse=True)
def cleanup_compiled_vnnlib():
    """Cleans up any .vnnlib.compiled files that get left behind by abcrown."""
    yield

    abs_path = get_file_path(Path(__file__))
    dir_name = abs_path / "trivial/"

    for item in os.listdir(dir_name):
        if item.endswith(".vnnlib.compiled"):
            os.remove(dir_name / item)


@pytest.fixture
def abcrown() -> AbCrown:
    return AbCrown()


@pytest.mark.gpu_prop
def test_sat(abcrown: AbCrown, trivial_sat: VerificationInstance):
    result = abcrown.verify_property(trivial_sat.property, trivial_sat.network)

    assert isinstance(result, Ok)
    assert result.value.result == "SAT"


@pytest.mark.gpu_prop
def test_unsat(abcrown: AbCrown, trivial_unsat: VerificationInstance):
    result = abcrown.verify_property(
        trivial_unsat.property, trivial_unsat.network
    )

    assert isinstance(result, Ok)
    assert result.value.result == "UNSAT"


@pytest.mark.gpu_prop
def test_err(abcrown: AbCrown):
    result = abcrown.verify_property(Path(), Path())

    assert isinstance(result, Err)
