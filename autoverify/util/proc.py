"""Utilities for process and CPU stuff."""
import os
import shlex
import subprocess
from typing import Iterable


# Credits: @jfs
def pid_exists(pid: int) -> bool:
    """Returns if the given PID exists."""
    if pid < 0:
        return False  # NOTE: pid == 0 returns True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:  # errno.ESRCH
        return False  # No such process
    except PermissionError:  # errno.EPERM
        return True  # Operation not permitted (i.e., process exists)
    else:
        return True  # no error, we can send a signal to the process


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


def nvidia_gpu_count() -> int:
    """Get the number of available NVIDIA GPUs."""
    cmd = "nvidia-smi --query-gpu=name --format=csv,noheader"
    cmd2 = "wc -l"

    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    count = (
        subprocess.check_output(shlex.split(cmd2), stdin=ps.stdout)
        .decode()
        .rstrip()
    )

    return int(count)


def taskset_cpu_range(cpus: Iterable[int] | tuple[int, int]):
    """Make a taskset command with the specified CPUs."""
    template = "taskset --cpu-list {}"

    if isinstance(cpus, tuple):
        cpus = [i for i in range(cpus[0], cpus[1] + 1)]

    return template.format(",".join(str(c) for c in cpus))
