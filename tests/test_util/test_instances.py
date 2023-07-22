from dataclasses import dataclass

import pytest

from autoverify.util.instances import (
    VerificationDataResult,
    VerificationInstance,
    get_dataclass_field_names,
)


@pytest.fixture
def vdr() -> VerificationDataResult:
    return VerificationDataResult(
        "network.onnx",
        "property.vnnlib",
        60,
        "nnenum",
        "a config",
        "OK",
        "SAT",
        10.0,
        "a counter example",
        "an error string",
    )


def test_as_smac_instance(trivial_sat: VerificationInstance):
    smac_inst = trivial_sat.as_smac_instance()
    net, prop, to = smac_inst.split(",")

    assert net is not None
    assert prop is not None
    assert to is not None


def test_get_dataclass_field_names():
    @dataclass
    class ADataclass:
        name: str
        age: int

    assert get_dataclass_field_names(ADataclass) == ["name", "age"]

    with pytest.raises(ValueError, match="Argument data_cls should be a class"):
        get_dataclass_field_names("Not a class")

    class NotADataclass:
        name: str
        age: int

    with pytest.raises(ValueError, match="'NotADataclass' is not a dataclass"):
        get_dataclass_field_names(NotADataclass)


def test_vdr_csv_row(vdr: VerificationDataResult):
    assert vdr.as_csv_row() == [
        "network.onnx",
        "property.vnnlib",
        "60",
        "nnenum",
        "a config",
        "OK",
        "SAT",
        "10.0",
        "a counter example",
        "an error string",
    ]

    vdr.counter_example = ("a", "counter example")
    assert vdr.as_csv_row() == [
        "network.onnx",
        "property.vnnlib",
        "60",
        "nnenum",
        "a config",
        "OK",
        "SAT",
        "10.0",
        "a\ncounter example",
        "an error string",
    ]
