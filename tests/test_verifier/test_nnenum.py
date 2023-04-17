import pytest
from result import Ok

from autoverify.verifier import Nnenum

from .conftest import VerificationInstance


@pytest.fixture
def nnenum() -> Nnenum:
    return Nnenum()


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
