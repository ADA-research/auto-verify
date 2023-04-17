from pathlib import Path

import pytest
from result import Ok

from autoverify.verifier import Nnenum

from ..util import run_av_cli
from .conftest import VerificationInstance


@pytest.fixture
def nnenum() -> Nnenum:
    return Nnenum()


# TODO: Needs proper cleanup mechanisms
def test_install_nnenum(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    output = run_av_cli(["--install", "nnenum"])

    yield output.find("Succesfully installed") >= 0

    output = run_av_cli(["--uninstall", "nnenum"])

    assert output.find("Succesfully uninstalled") >= 0


def test_sat(nnenum: Nnenum, trivial_sat: VerificationInstance):
    result = nnenum.verify_property(trivial_sat.property, trivial_sat.network)

    assert isinstance(result, Ok)
    assert result.value.result == "SAT"


def test_unsat(nnenum: Nnenum, trivial_unsat: VerificationInstance):
    result = nnenum.verify_property(
        trivial_unsat.property, trivial_unsat.network
    )

    assert isinstance(result, Ok)
    assert result.value.result == "UNSAT"
