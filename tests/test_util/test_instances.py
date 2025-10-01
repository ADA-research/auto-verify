from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import pytest

from autoverify.util.instances import (
    VerificationDataResult,
    VerificationInstance,
    _passes_all,
    _passes_at_least_1,
    csv_append_verification_result,
    get_dataclass_field_names,
    init_verification_result_csv,
    read_all_vnncomp_instances,
    read_verification_result_from_csv,
    read_vnncomp_instances,
    unique_networks,
    verification_instances_to_smac_instances,
    write_verification_results_to_csv,
)
from autoverify.verifier.verification_result import CompleteVerificationData


def read_csv_contents(csv_path: Path) -> str:
    with open(str(csv_path)) as csv_file:
        return csv_file.read()


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
        "some output",
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
        "some output",
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
        "some output",
    ]


def test_vdr_from_verif_res(complete_verif_data: CompleteVerificationData):
    v = VerificationDataResult.from_verification_result(
        complete_verif_data,
        {
            "network": "hello",
            "property": "world",
            "timeout": 42,
            "verifier": "nnenum",
            "config": None,
            "success": "OK",
        },
    )

    assert v


@pytest.mark.parametrize(
    "vis",
    [
        [VerificationInstance(Path("fake_net.onnx"), Path("fake_prop.vnnlib"), 180)],
        [
            VerificationInstance(Path("fake_net.onnx"), Path("fake_prop.vnnlib"), 180),
            VerificationInstance(Path("fake_net.onnx"), Path("fake_prop.vnnlib"), 180),
        ],
        [],
    ],
)
def test_verif_inst_to_smac_inst(vis: list[VerificationInstance]):
    smac_inst = verification_instances_to_smac_instances(vis)

    assert len(vis) == len(smac_inst)
    if len(vis) == 0:
        return

    assert len(smac_inst[0].split(",")) == 3
    assert smac_inst[0] == "fake_net.onnx,fake_prop.vnnlib,180"


def test_init_verification_result_csv(tmp_path: Path):
    tmp_csv = tmp_path / "tmp.csv"

    init_verification_result_csv(tmp_csv)

    assert tmp_csv.exists()

    expected_header = ",".join(get_dataclass_field_names(VerificationDataResult)) + "\n"
    assert read_csv_contents(tmp_csv) == expected_header


def test_append_verification_result(tmp_path: Path, vdr: VerificationDataResult):
    tmp_csv = tmp_path / "tmp.csv"
    init_verification_result_csv(tmp_csv)
    csv_append_verification_result(vdr, tmp_csv)

    expected_header = ",".join(get_dataclass_field_names(VerificationDataResult)) + "\n"
    expected_row = (
        ",".join(
            [
                "network.onnx",
                "property.vnnlib",
                str(60),
                "nnenum",
                "a config",
                "OK",
                "SAT",
                str(10.0),
                "a counter example",
                "an error string",
                "some output",
            ]
        )
        + "\n"
    )

    assert read_csv_contents(tmp_csv) == expected_header + expected_row


def test_read_verification_result_from_csv(tmp_path: Path, vdr: VerificationDataResult):
    tmp_csv = tmp_path / "tmp.csv"
    init_verification_result_csv(tmp_csv)
    csv_append_verification_result(vdr, tmp_csv)
    csv_append_verification_result(vdr, tmp_csv)

    vdrs = read_verification_result_from_csv(tmp_csv)
    assert vdrs == [vdr, vdr]


def test_write_verification_result_from_csv(tmp_path: Path, vdr: VerificationDataResult):
    tmp_csv = tmp_path / "tmp.csv"
    tmp_csv2 = tmp_path / "tmp2.csv"
    init_verification_result_csv(tmp_csv)
    init_verification_result_csv(tmp_csv2)
    csv_append_verification_result(vdr, tmp_csv)
    csv_append_verification_result(vdr, tmp_csv)

    results_df = pd.read_csv(tmp_csv)
    write_verification_results_to_csv(results_df, tmp_csv2)

    assert read_verification_result_from_csv(tmp_csv) == read_verification_result_from_csv(tmp_csv2)


def test_read_vnncomp_instances():
    vnncomp_path = Path(__file__).parent.parent / "fake_vnncomp"
    bench_name = "trivial"
    assert vnncomp_path.is_dir()

    instances = read_vnncomp_instances(bench_name, vnncomp_path)
    assert len(instances) == 6

    def _check_path(p: Path) -> bool:
        return (vnncomp_path / bench_name / p).is_file()

    for inst in instances:
        assert _check_path(inst.network)
        assert _check_path(inst.property)
        assert inst.timeout

    instances = read_vnncomp_instances(bench_name, vnncomp_path, as_smac=True)
    assert len(instances) == 6

    for inst in instances:
        net, prop, timeout = inst.split(",")
        assert _check_path(Path(net))
        assert _check_path(Path(prop))
        assert timeout

    def _nano_filter(inst: VerificationInstance) -> bool:
        return inst.network.name == "test_nano.onnx"

    def _sat_filter(inst: VerificationInstance) -> bool:
        return inst.network.name == "test_sat.onnx"

    instances = read_vnncomp_instances(bench_name, vnncomp_path, predicate=_nano_filter)
    assert len(instances) == 2

    instances = read_vnncomp_instances(bench_name, vnncomp_path, predicate=[_nano_filter, _sat_filter])
    assert len(instances) == 4

    with pytest.raises(ValueError):
        read_vnncomp_instances(bench_name, Path("this_is_not_a_dir.txt"))


def test_read_all_vnncomp_instances():
    vnncomp_path = Path(__file__).parent.parent / "fake_vnncomp"
    instances = read_all_vnncomp_instances(vnncomp_path)

    assert "trivial" in instances
    assert "trivial_clone" in instances


def test_unique_networks():
    vnncomp_path = Path(__file__).parent.parent / "fake_vnncomp"
    instances = read_all_vnncomp_instances(vnncomp_path)["trivial"]
    assert len(instances) == 6

    instances = unique_networks(instances)
    assert len(instances) == 3


def test_passes(trivial_sat: VerificationInstance):
    def _predicate_false(*_):
        return False

    def _predicate_true(*_):
        return True

    assert _passes_all([_predicate_true], trivial_sat)
    assert not _passes_all([_predicate_false], trivial_sat)
    assert _passes_at_least_1([_predicate_true], trivial_sat)
    assert not _passes_at_least_1([_predicate_false], trivial_sat)
