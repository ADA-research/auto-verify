from pathlib import Path

import pytest
from ConfigSpace import ConfigurationSpace, Integer

from autoverify.util.env import get_file_path
from autoverify.util.instances import VerificationInstance
from autoverify.verifier import AbCrown, Nnenum, OvalBab, Verinet
from autoverify.verifier.verifier import CompleteVerifier

TEST_PROP_TIMEOUT = 60
test_props = get_file_path(Path(__file__)) / "test_props/"


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
        property=test_props / "test_nano.vnnlib",
        network=test_props / "test_nano.onnx",
        timeout=TEST_PROP_TIMEOUT,
    )


@pytest.fixture
def trivial_sat() -> VerificationInstance:
    return VerificationInstance(
        property=test_props / "test_prop.vnnlib",
        network=test_props / "test_sat.onnx",
        timeout=TEST_PROP_TIMEOUT,
    )


@pytest.fixture
def trivial_unsat() -> VerificationInstance:
    return VerificationInstance(
        property=test_props / "test_prop.vnnlib",
        network=test_props / "test_unsat.onnx",
        timeout=TEST_PROP_TIMEOUT,
    )


@pytest.fixture
def nnenum() -> Nnenum:
    return Nnenum()


@pytest.fixture
def abcrown() -> AbCrown:
    return AbCrown()


@pytest.fixture
def verinet() -> Verinet:
    return Verinet()


@pytest.fixture
def ovalbab() -> OvalBab:
    return OvalBab()


#
#
# @pytest.fixture
# def cpu_verifiers(nnenum: Nnenum) -> list[CompleteVerifier]:
#     return [nnenum]
#
#
# @pytest.fixture
# def gpu_verifiers(
#     abcrown: AbCrown,
#     mnbab: MnBab,
#     ovalbab: OvalBab,
# ) -> list[CompleteVerifier]:
#     return [abcrown, mnbab, ovalbab]
