import pytest

from autoverify.util.proc import taskset_cpu_range


def test_taskset_cpu_range():
    cpus_iterable = [1, 2, 3]
    result = taskset_cpu_range(cpus_iterable)
    assert result == "taskset --cpu-list 1,2,3"

    cpus_range = (1, 3)
    result = taskset_cpu_range(cpus_range)
    assert result == "taskset --cpu-list 1,2,3"

    empty_iterable = []
    with pytest.raises(ValueError):
        result = taskset_cpu_range(empty_iterable)

    single_cpu = [5]
    result = taskset_cpu_range(single_cpu)
    assert result == "taskset --cpu-list 5"

    large_range = (1, 100)
    result = taskset_cpu_range(large_range)
    expected_result = "taskset --cpu-list " + ",".join(map(str, range(1, 101)))
    assert result == expected_result
