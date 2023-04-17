import pytest

from autoverify.verifier import Nnenum

from .conftest import VerificationInstance


@pytest.fixture
def nnenum() -> Nnenum:
    return Nnenum()


def test_idk(nnenum: Nnenum, trivial_nano: VerificationInstance):
    result = nnenum.verify_property(trivial_nano.property, trivial_nano.network)
    print(result)
    assert 0
