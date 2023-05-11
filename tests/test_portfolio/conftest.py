import pytest

from autoverify.util.instances import (
    VerificationInstance,
    read_vnncomp_instances,
)


@pytest.fixture
def mnist_instances() -> list[VerificationInstance]:
    return read_vnncomp_instances("mnist_fc")


@pytest.fixture
def acasxu_instances() -> list[VerificationInstance]:
    return read_vnncomp_instances("acasxu")
