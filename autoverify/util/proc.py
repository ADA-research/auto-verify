"""Utilities for process and CPU stuff."""
import os
import shlex
import subprocess
from collections.abc import Collection
from typing import Iterable, Sequence


def pkill_match(pattern: str):
    """Kill processes matching the pattern."""
    cmd = f'pkill -f "{pattern}"'

    result = subprocess.run(shlex.split(cmd))

    # pkill has non standard exitcodes (`man pkill`):
    # 0      One or more processes matched the criteria
    # 1      No processes matched
    # 2      Syntax error
    # 3      Fatal error
    if result.returncode > 1:
        raise Exception(result.stderr)


def cpu_count() -> int:
    """Return the number of available CPUs."""
    return len(os.sched_getaffinity(0))


def taskset_cpu_range(cpus: Iterable[int] | tuple[int, int]):
    """Make a taskset command with the specified CPUs."""
    template = "taskset --cpu-list {}"

    if isinstance(cpus, tuple):
        cpus = [i for i in range(cpus[0], cpus[1] + 1)]

    return template.format(",".join(str(c) for c in cpus))
