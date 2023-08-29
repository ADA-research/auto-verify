"""_summary_."""
from typing import TypeVar

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio
from autoverify.util.instances import VerificationDataResult
from autoverify.util.proc import cpu_count, nvidia_gpu_count
from autoverify.util.verification_instance import VerificationInstance

_VI = TypeVar("_VI", VerificationInstance, str)


class PortfolioRunner:
    """_summary_."""

    def __init__(self, portfolio: Portfolio):
        """_summary_."""
        self._portfolio = portfolio
        self._init_resources()

    def _init_resources(self):
        # TODO:
        #
        # - [/] Sanity check resources
        # - [/] Allocate the CPU and GPU numbers
        self._allocation: dict[ConfiguredVerifier, tuple[int, int, int]] = {}
        cpu_left, gpu_left = cpu_count(), nvidia_gpu_count()

        for cv in self._portfolio:
            if cv.resources is None:
                raise ValueError(
                    "No resources for"
                    f"{cv.verifier} :: {cv.configuration} found."
                )

            # CPU (taskset) and GPU (CUDA_VISIBLE_DEVICES) index start at 0
            n_cpu, n_gpu = cv.resources[0], cv.resources[1]

            # Currently only support 1 GPU per verifier
            if n_gpu > 0:
                curr_gpu = gpu_left
                gpu_left -= 1
            else:
                curr_gpu = -1

            cpu_high = cpu_left
            cpu_low = cpu_left - n_cpu
            cpu_left = cpu_low

            self._allocation[cv] = (cpu_low, cpu_high - 1, curr_gpu)

    def verify_instances(
        self, instances: list[_VI]
    ) -> dict[_VI, VerificationDataResult]:
        """_summary_."""
        # TODO:
        #     - launch all verifiers in parallel
        #     - as soon as one finds a result:
        #       - save result
        #       - stop all verifiers
        #     - go to next instance
        results: dict[_VI, VerificationDataResult] = {}

        return results
