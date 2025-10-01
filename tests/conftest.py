from pathlib import Path

import pytest
from ConfigSpace import (
    Categorical,
    Configuration,
    ConfigurationSpace,
    Float,
    Integer,
)
from result import Err, Ok
from smac import RunHistory

from autoverify.util.env import get_file_path
from autoverify.util.instances import VerificationInstance
from autoverify.verifier import AbCrown, MnBab, Nnenum, OvalBab, Verinet
from autoverify.verifier.verification_result import (
    CompleteVerificationData,
    CompleteVerificationResult,
)

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
def simple_config(simple_configspace: ConfigurationSpace) -> Configuration:
    return simple_configspace.sample_configuration()


@pytest.fixture
def runhistory(simple_configspace: ConfigurationSpace) -> RunHistory:
    cfg1, cfg2 = simple_configspace.sample_configuration(2)

    rh = RunHistory()
    rh.add(cfg1, 10.0, instance="foo")
    rh.add(cfg2, 20.0, instance="bar")

    return rh


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
def mnbab() -> MnBab:
    return MnBab()


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


@pytest.fixture
def err_verif_data() -> CompleteVerificationData:
    """Create a CompleteVerificationData with ERR result."""
    return CompleteVerificationData(
        result="ERR",
        took=15.0,
        counter_example=None,
        err="Verification tool crashed with exit code 1",
        stdout="Error: Invalid input format\nTraceback (most recent call last):\n...",
    )


@pytest.fixture
def err_verif_res(
    err_verif_data: CompleteVerificationData,
) -> CompleteVerificationResult:
    """Create a CompleteVerificationResult with ERR data."""
    return Ok(err_verif_data)
