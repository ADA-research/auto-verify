"""_summary_."""
import concurrent.futures
import logging
from typing import TypeVar

from result import Err, Ok

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio
from autoverify.util.instances import VerificationDataResult
from autoverify.util.proc import cpu_count, nvidia_gpu_count
from autoverify.util.resources import to_allocation
from autoverify.util.verification_instance import VerificationInstance
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp import inst_bench_to_verifier
from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier

logger = logging.getLogger(__name__)

_VI = TypeVar("_VI", VerificationInstance, str)
_CostDict = dict[ConfiguredVerifier, dict[VerificationInstance, float]]

# Instance -> (min cost, verifier (whose cost that is))
_VbsResult = dict[str, tuple[float, str]]


def _get_verifier(
    instance: VerificationInstance,
    cv: ConfiguredVerifier,
    vnncompat: bool,
    benchmark: str | None,
) -> CompleteVerifier:
    if vnncompat:
        assert benchmark and cv.resources
        return inst_bench_to_verifier(
            benchmark, instance, cv.verifier, to_allocation(cv.resources)
        )
    else:
        if cv.resources:
            v = verifier_from_name(cv.verifier)(
                cpu_gpu_allocation=to_allocation(cv.resources)
            )
        else:
            v = verifier_from_name(cv.verifier)()

        assert isinstance(v, CompleteVerifier)
        return v


class PortfolioRunner:
    """_summary_."""

    def __init__(self, portfolio: Portfolio, vbs_mode: bool = False):
        """_summary_."""
        self._portfolio = portfolio
        self._vbs_mode = vbs_mode

        if not self._vbs_mode:
            self._init_resources()

    def _init_resources(self):
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

            if n_gpu > gpu_left:
                raise RuntimeError("No more GPUs left")
            if n_cpu > cpu_left:
                raise RuntimeError("No more CPUs left")
            if n_cpu <= 0:
                raise RuntimeError("CPUs should be > 0")

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

    def evaluate_vbs(
        self,
        instances: list[VerificationInstance],
        *,
        vnncompat: bool = False,
        benchmark: str | None = None,
    ) -> _VbsResult:
        """_summary_."""
        results: _CostDict = {}

        if vnncompat and benchmark is None:
            raise ValueError("Need a benchmark if vnncompat=True")
        elif not vnncompat and benchmark is not None:
            raise ValueError("Only use benchmark if vnncompat=True")

        for cv in self._portfolio:
            assert cv.resources is not None

            for instance in instances:
                verifier = _get_verifier(instance, cv, vnncompat, benchmark)
                logger.info(f"{cv.verifier} on {str(instance)}")
                result = verifier.verify_instance(instance)
                self._add_result(cv, instance, result, results)

        return self._vbs_from_cost_dict(results)

    @staticmethod
    def _vbs_from_cost_dict(cost_dict: _CostDict) -> _VbsResult:
        vbs: _VbsResult = {}

        for cv, instance_costs in cost_dict.items():
            for instance, cost in instance_costs.items():
                instance = str(instance)

                if instance not in vbs:
                    vbs[instance] = (cost, cv.verifier)
                    continue

                if cost < vbs[instance][0]:
                    vbs[instance] = (cost, cv.verifier)

        return vbs

    @staticmethod
    def _add_result(
        cv: ConfiguredVerifier,
        instance: VerificationInstance,
        result: CompleteVerificationResult,
        results: _CostDict,
    ):
        cost: float

        if isinstance(result, Ok):
            cost = result.unwrap().took
        elif isinstance(result, Err):
            cost = float("inf")

        logger.info(f"Cost: {cost}")

        if cv not in results:
            results[cv] = {}

        results[cv][instance] = cost

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
        if self._vbs_mode:
            raise RuntimeError("Function not compatible with vbs_mode")

        results: dict[_VI, VerificationDataResult] = {}

        for cv in self._portfolio:
            print(cv)

        return results
