"""Test trivial props to see if verifiers work."""
import os
from pathlib import Path

import pytest
from result import Err, Ok

from autoverify.util.env import get_file_path
from autoverify.verifier.verifier import CompleteVerifier

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


def run_trivial_sat(
    verifier: CompleteVerifier,
    trivial_sat: VerificationInstance,
):
    result = verifier.verify_property(trivial_sat.property, trivial_sat.network)

    assert isinstance(result, Ok)
    assert result.value.result == "SAT"


def run_trivial_unsat(
    verifier: CompleteVerifier,
    trivial_unsat: VerificationInstance,
):
    result = verifier.verify_property(
        trivial_unsat.property, trivial_unsat.network
    )

    assert isinstance(result, Ok)
    assert result.value.result == "UNSAT"


def run_trivial_err(verifier: CompleteVerifier):
    result = verifier.verify_property(Path(), Path())

    assert isinstance(result, Err)


@pytest.mark.cpu_prop
def test_cpu_verifiers(
    cpu_verifiers: list[CompleteVerifier],
    trivial_sat: VerificationInstance,
    trivial_unsat: VerificationInstance,
):
    for verifier in cpu_verifiers:
        run_trivial_sat(verifier, trivial_sat)
        run_trivial_unsat(verifier, trivial_unsat)
        run_trivial_err(verifier)


@pytest.mark.gpu_prop
def test_gpu_verifiers(
    gpu_verifiers: list[CompleteVerifier],
    trivial_sat: VerificationInstance,
    trivial_unsat: VerificationInstance,
):
    for verifier in gpu_verifiers:
        run_trivial_sat(verifier, trivial_sat)
        run_trivial_unsat(verifier, trivial_unsat)
        run_trivial_err(verifier)
