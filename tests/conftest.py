from pathlib import Path

import pytest
from ConfigSpace import ConfigurationSpace, Integer

from autoverify.util.env import get_file_path
from autoverify.util.instances import VerificationInstance
from autoverify.verifier import AbCrown, MnBab, Nnenum, OvalBab
from autoverify.verifier.verifier import CompleteVerifier

trivial = get_file_path(Path(__file__)) / "test_verifier/trivial/"


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "cpu_prop: mark test as cpu nn prop tests"
    )

    config.addinivalue_line(
        "markers", "gpu_prop: mark test as gpu nn prop tests"
    )


@pytest.fixture
def simple_configspace() -> ConfigurationSpace:
    config_space = ConfigurationSpace()
    config_space.add_hyperparameters(
        [
            Integer("number", (1, 1000), default=500),
        ]
    )

    return config_space


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
def mnbab() -> MnBab:
    return MnBab()


@pytest.fixture
def ovalbab() -> OvalBab:
    return OvalBab()


@pytest.fixture
def cpu_verifiers(nnenum: Nnenum) -> list[CompleteVerifier]:
    return [nnenum]


@pytest.fixture
def gpu_verifiers(
    abcrown: AbCrown,
    mnbab: MnBab,
    ovalbab: OvalBab,
) -> list[CompleteVerifier]:
    return [abcrown, mnbab, ovalbab]
