import shlex
import subprocess

from autoverify.portfolio.portfolio import PortfolioScenario
from autoverify.util.proc import cpu_count
from autoverify.util.resource_strategy import ResourceStrategy


class ResourceTracker:
    def __init__(
        self,
        pf_scen: PortfolioScenario,
        *,
        strategy: ResourceStrategy | str = ResourceStrategy.Auto,
    ):
        self._verifiers = pf_scen.verifiers
        self._verifier_resources = pf_scen.resources
        self._pf_len = pf_scen.length

        if isinstance(strategy, str):
            strategy = ResourceStrategy(strategy)
        self._strategy = strategy
        self._init_strat()

    def _init_strat(self):
        if self._strategy == ResourceStrategy.Auto:
            self._resources = (cpu_count(), nvidia_gpu_count())
            self._cpus_per = self._resources[0] // self._pf_len
            self._cpus_remainder = self._resources[0] % self._pf_len
        else:
            raise NotImplementedError

    def get_possible(self) -> list[str]:
        """_summary_."""
        possible: list[str] = []

        if self._strategy == ResourceStrategy.Auto:
            possible = self._get_possible_auto()
        else:
            # TODO:
            raise NotImplementedError

        return possible

    def deduct(self, resources: tuple[int, int]):
        """_summary_."""
        self._resources = (
            self._resources[0] - resources[0],
            self._resources[1] - resources[1],
        )

    def deduct_from_name(self, name: str):
        """_summary_."""
        for vr in self._verifier_resources:
            if vr[0] == name:
                cpus_to_deduct = self._cpus_per
                gpus_to_deduct = vr[2]

                if self._cpus_remainder > 0:
                    cpus_to_deduct += 1
                    self._cpus_remainder -= 1

                self.deduct((cpus_to_deduct, gpus_to_deduct))

    def _get_possible_auto(self) -> list[str]:
        """Auto strategy.

        Every verifier gets `n_cpu / pf_len` cores, GPUs are
        assigned 1 per.
        """
        possible: list[str] = []
        _, gpu_left = self._resources

        for v in self._verifier_resources:
            if gpu_left < v[2]:
                continue

            possible.append(v[0])

        return possible


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
