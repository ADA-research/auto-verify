"""_summary_."""

from autoverify.portfolio.portfolio import PortfolioScenario
from autoverify.util.proc import cpu_count, nvidia_gpu_count
from autoverify.util.resource_strategy import ResourceStrategy


def to_allocation(resources: tuple[int, int]) -> tuple[int, int, int]:
    """Go from (n_cpu, n_gpu) to a real allocation."""
    gpu = -1 if resources[1] <= 0 else resources[1] - 1
    return (0, resources[0] - 1, gpu)


class ResourceTracker:
    """Class to track available resources."""

    def __init__(
        self,
        pf_scen: PortfolioScenario,
        *,
        strategy: ResourceStrategy | str = ResourceStrategy.Auto,
        cpu_gpu_count: tuple[int, int] | None = None,
    ):
        """Create a new resource tracker.

        Arguments:
            pf_scen: The PF scenario being used.
            strategy: The resource strategy to use during alloc.
            cpu_gpu_count: Override the number of CPU/GPUs.
        """
        self._verifiers = pf_scen.verifiers
        self._verifier_resources = pf_scen.resources
        self._pf_len = pf_scen.length
        self._cpu_gpu_count = cpu_gpu_count

        if isinstance(strategy, str):
            strategy = ResourceStrategy(strategy)
        self._strategy = strategy
        self._init_strat()

    def _init_strat(self):
        if self._strategy == ResourceStrategy.Auto:
            if self._cpu_gpu_count is None:
                self._resources = (cpu_count(), nvidia_gpu_count())
            else:
                self._resources = self._cpu_gpu_count
            self._cpus_per = self._resources[0] // self._pf_len
            self._cpus_remainder = self._resources[0] % self._pf_len
        else:
            raise NotImplementedError

    @property
    def resources(self):
        return self._resources

    def get_possible(self) -> list[str]:
        """Get the verifiers that still fit in the PF."""
        possible: list[str] = []

        if self._strategy == ResourceStrategy.Auto:
            possible = self._get_possible_auto()
        else:
            # TODO:
            raise NotImplementedError

        return possible

    def deduct(self, resources: tuple[int, int]):
        """Deduct resources after adding to the PF."""
        self._resources = (
            self._resources[0] - resources[0],
            self._resources[1] - resources[1],
        )

    # TODO: Respect strategy
    def deduct_by_name(
        self,
        name: str,
        *,
        mock: bool = False,
    ) -> tuple[int, int]:
        """Deduct based on the name, mock to see what would be left."""
        to_deduct: tuple[int, int] = (0, 0)

        for vr in self._verifier_resources:
            if vr[0] == name:
                cpus_to_deduct = self._cpus_per
                gpus_to_deduct = vr[2]

                if self._cpus_remainder > 0:
                    cpus_to_deduct += 1
                    self._cpus_remainder -= 1

                to_deduct = (cpus_to_deduct, gpus_to_deduct)

                if not mock:
                    self.deduct(to_deduct)

        return to_deduct

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
