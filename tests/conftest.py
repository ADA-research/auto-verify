from pathlib import Path

import pytest
from ConfigSpace import Categorical, ConfigurationSpace, Float, Integer
from result import Err, Ok

from autoverify.util.env import get_file_path
from autoverify.util.instances import VerificationInstance
from autoverify.verifier import AbCrown, Nnenum, OvalBab, Verinet
from autoverify.verifier.verification_result import (
    CompleteVerificationData,
    CompleteVerificationResult,
)
from autoverify.verifier.verifier import CompleteVerifier

TEST_PROP_TIMEOUT = 60
test_props = get_file_path(Path(__file__)) / "trivial_props/"


@pytest.fixture
def simple_configspace() -> ConfigurationSpace:
    config_space = ConfigurationSpace()
    config_space.add_hyperparameters(
        [
            Integer("A", (1, 1000), default=500),
            Float("B", (1.0, 10.0), default=5.0),
            Categorical("C", [True, False], default=True),
        ]
    )

    return config_space


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
def trivial_timeout() -> VerificationInstance:
    return VerificationInstance(
        property=test_props / "test_prop.vnnlib",
        network=test_props / "test_sat.onnx",
        timeout=0,
    )


@pytest.fixture
def trivial_nano() -> VerificationInstance:
    return VerificationInstance(
        property=test_props / "test_nano.vnnlib",
        network=test_props / "test_nano.onnx",
        timeout=TEST_PROP_TIMEOUT,
    )


@pytest.fixture
def trivial_instances(
    trivial_sat: VerificationInstance,
    trivial_unsat: VerificationInstance,
    trivial_nano: VerificationInstance,
) -> list[VerificationInstance]:
    return [trivial_sat, trivial_unsat, trivial_nano]


@pytest.fixture
def nnenum() -> Nnenum:
    return Nnenum()


@pytest.fixture
def abcrown() -> AbCrown:
    return AbCrown()


# Verinet fails on trivial props without these init args
# and it still fails on nano
@pytest.fixture
def verinet() -> Verinet:
    return Verinet(dnnv_simplify=False, transpose_matmul_weights=True)


@pytest.fixture
def ovalbab() -> OvalBab:
    return OvalBab()


@pytest.fixture
def complete_verif_data() -> CompleteVerificationData:
    return CompleteVerificationData(
        result="SAT",
        took=42.0,
        counter_example="hello counter example",
        err="a dummy error",
        stdout="some output",
    )


@pytest.fixture
def ok_complete_verif_res(
    complete_verif_data: CompleteVerificationData,
) -> CompleteVerificationResult:
    return Ok(complete_verif_data)


@pytest.fixture
def timeout_complete_verif_res(
    complete_verif_data: CompleteVerificationData,
) -> CompleteVerificationResult:
    complete_verif_data.result = "TIMEOUT"
    return Ok(complete_verif_data)


@pytest.fixture
def err_complete_verif_res(
    complete_verif_data: CompleteVerificationData,
) -> CompleteVerificationResult:
    return Err(complete_verif_data)
