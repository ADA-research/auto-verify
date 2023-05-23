"""Utilities for process and CPU stuff."""
import os
import shlex
import subprocess


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
