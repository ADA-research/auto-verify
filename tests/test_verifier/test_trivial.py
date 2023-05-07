"""Test trivial props to see if verifiers work."""
import os
from pathlib import Path

import pytest
from pytest_lazyfixture import lazy_fixture
from result import Err, Ok

from autoverify.util.env import get_file_path
from autoverify.verifier.verifier import CompleteVerifier

from .conftest import VerificationInstance

# TODO: Move the ajray with verifier fixtures to a place where other files can
# acccess it as well
pytestmark = pytest.mark.parametrize(
    "verifier",
    [
        pytest.param(lazy_fixture("nnenum"), marks=pytest.mark.cpu_only),
        pytest.param(lazy_fixture("abcrown"), marks=pytest.mark.uses_gpu),
        # pytest.param(lazy_fixture("mnbab"), marks=pytest.mark.uses_gpu),
        pytest.param(lazy_fixture("ovalbab"), marks=pytest.mark.uses_gpu),
    ],
)


@pytest.fixture(autouse=True)
def cleanup_compiled_vnnlib():
    """Cleans up any .vnnlib.compiled files that get left behind."""
    yield

    abs_path = get_file_path(Path(__file__))
    dir_name = abs_path / "trivial/"

    for item in os.listdir(dir_name):
        if item.endswith(".vnnlib.compiled"):
            os.remove(dir_name / item)


def test_sat(
    verifier: CompleteVerifier,
    trivial_sat: VerificationInstance,
):
    result = verifier.verify_property(trivial_sat.network, trivial_sat.property)

    assert isinstance(result, Ok)
    assert result.value.result == "SAT"


def test_unsat(
    verifier: CompleteVerifier,
    trivial_unsat: VerificationInstance,
):
    result = verifier.verify_property(
        trivial_unsat.network, trivial_unsat.property
    )

    assert isinstance(result, Ok)
    assert result.value.result == "UNSAT"


def test_err(verifier: CompleteVerifier):
    result = verifier.verify_property(Path(), Path())

    assert isinstance(result, Err)
