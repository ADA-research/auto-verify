import pytest

from benchmarks.util import read_vnncomp_instances


@pytest.fixture
def mnist_instances() -> list[str]:
    return read_vnncomp_instances("mnist_fc")


@pytest.fixture
def acasxu_instances() -> list[str]:
    return read_vnncomp_instances("acasxu")
