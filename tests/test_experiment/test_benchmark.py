import pytest

from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.path import check_file_extension


@pytest.mark.parametrize(
    "benchmark,length",
    [
        ("mnist_fc", 90),
        ("acasxu", 186),
    ],
)
def test_read_vnncomp_benchmark(benchmark: str, length: int):
    mnist_fc = read_vnncomp_instances(benchmark)
    instance = mnist_fc[0]

    assert check_file_extension(instance.network, ".onnx")
    assert check_file_extension(instance.property, ".vnnlib")

    assert isinstance(instance.timeout, int)
    assert instance.timeout > 0

    assert len(mnist_fc) == length
