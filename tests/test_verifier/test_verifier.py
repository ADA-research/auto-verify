import os
from pathlib import Path

import pytest
from pytest_lazyfixture import lazy_fixture
from result import Ok

from autoverify.util.env import get_file_path
from autoverify.util.instances import VerificationInstance
from autoverify.verifier.verifier import CompleteVerifier

pytestmark = pytest.mark.parametrize(
    "verifier",
    [
        pytest.param(lazy_fixture("nnenum")),
        pytest.param(lazy_fixture("abcrown")),
        pytest.param(lazy_fixture("ovalbab")),
        pytest.param(lazy_fixture("verinet")),
    ],
)


@pytest.fixture(autouse=True)
def cleanup_compiled_vnnlib():
    """Cleans up any .vnnlib.compiled files that get left behind."""
    yield

    abs_path = get_file_path(Path(__file__))
    dir_name = abs_path / "../trivial_props/"

    for item in os.listdir(dir_name):
        if item.endswith(".vnnlib.compiled"):
            os.remove(dir_name / item)


def test_sat(
    verifier: CompleteVerifier,
    trivial_sat: VerificationInstance,
):
    result = verifier.verify_instance(trivial_sat)

    assert isinstance(result, Ok)
    assert result.value.result == "SAT"


def test_unsat(
    verifier: CompleteVerifier,
    trivial_unsat: VerificationInstance,
):
    result = verifier.verify_instance(trivial_unsat)

    assert isinstance(result, Ok)
