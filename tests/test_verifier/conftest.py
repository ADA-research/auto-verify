from dataclasses import dataclass
from pathlib import Path

import pytest

from autoverify.util.env import get_file_path
from autoverify.verifier import AbCrown, Nnenum
from autoverify.verifier.verifier import CompleteVerifier

trivial = get_file_path(Path(__file__)) / "trivial/"


@dataclass
class VerificationInstance:
    property: Path
    network: Path


@pytest.fixture
def trivial_nano() -> VerificationInstance:
    return VerificationInstance(
        property=trivial / "test_nano.vnnlib",
        network=trivial / "test_nano.onnx",
    )


@pytest.fixture
def trivial_sat() -> VerificationInstance:
    return VerificationInstance(
        property=trivial / "test_prop.vnnlib",
        network=trivial / "test_sat.onnx",
    )


@pytest.fixture
def trivial_unsat() -> VerificationInstance:
    return VerificationInstance(
        property=trivial / "test_prop.vnnlib",
        network=trivial / "test_unsat.onnx",
    )


@pytest.fixture
def nnenum() -> Nnenum:
    return Nnenum()


@pytest.fixture
def abcrown() -> AbCrown:
    return AbCrown()


@pytest.fixture
def cpu_verifiers(nnenum: Nnenum) -> list[CompleteVerifier]:
    return [nnenum]


@pytest.fixture
def gpu_verifiers(abcrown: AbCrown) -> list[CompleteVerifier]:
    return [abcrown]
