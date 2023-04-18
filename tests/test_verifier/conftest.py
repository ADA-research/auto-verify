from dataclasses import dataclass
from pathlib import Path

import pytest

from autoverify.util.env import get_file_path

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
