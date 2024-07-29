"""Class to run parallel portfolio."""

import concurrent.futures
import logging
import signal
import sys
from collections.abc import Iterable
from concurrent.futures import Future
from pathlib import Path
from typing import Any

from ConfigSpace import Configuration
from result import Err, Ok

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio
from autoverify.util import set_iter_except
from autoverify.util.instances import (
    VerificationDataResult,
    csv_append_verification_result,
    init_verification_result_csv,
)
from autoverify.util.proc import cpu_count, nvidia_gpu_count
from autoverify.util.resources import to_allocation
from autoverify.util.verification_instance import VerificationInstance
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp import inst_bench_to_verifier
from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier

logger = logging.getLogger(__name__)

_CostDict = dict[ConfiguredVerifier, dict[VerificationInstance, float]]
# Instance -> (min cost, verifier (whose cost that is))
_VbsResult = dict[str, tuple[float, str]]


def _get_verifier(
    instance: VerificationInstance,
    cv: ConfiguredVerifier,
    vnncompat: bool,
    benchmark: str | None,
    verifier_kwargs: dict[str, dict[str, Any]] | None = None,
    cv_alloc: dict[ConfiguredVerifier, tuple[int, int, int]] | None = None,
) -> CompleteVerifier:
    if vnncompat:
        assert benchmark and cv.resources
        return inst_bench_to_verifier(
            benchmark, instance, cv.verifier, to_allocation(cv.resources)
        )
    else:
        alloc: tuple[int, int, int] | None
        if cv_alloc:
            alloc = cv_alloc[cv]
        else:
            alloc = to_allocation(cv.resources) if cv.resources else None

        kwargs = verifier_kwargs or {}
        kwargs = kwargs.get(cv.verifier, {})  # type: ignore

        v = verifier_from_name(cv.verifier)(
            cpu_gpu_allocation=alloc, **kwargs  # type: ignore
        )
        assert isinstance(v, CompleteVerifier)

        return v


class PortfolioRunner:
    """Class to run a portfolio in parallel."""

    def __init__(
        self,
        portfolio: Portfolio,
        vbs_mode: bool = False,
        *,
        n_cpu: int | None = None,
        n_gpu: int | None = None,
    ):
        """Initialize a new portfolio runner.

        Arguments:
            portfolio: The portfolio that will be run.
            vbs_mode: If the PF will be run in VBS mode.
            n_cpu: Override number of CPUs
            n_gpu: Override number of GPUs.
        """
        self._portfolio = portfolio
        self._vbs_mode = vbs_mode
        self._n_cpu = n_cpu
        self._n_gpu = n_gpu

        if not self._vbs_mode:
            self._init_resources()

        self._is_cleaning = False

        def _wrap_cleanup(*_):
            if self._is_cleaning:
                return

            self._is_cleaning = True
            self._cleanup()
            self._is_cleaning = False

        signal.signal(signal.SIGINT, _wrap_cleanup)
        signal.signal(signal.SIGTERM, _wrap_cleanup)

    def _init_resources(self):
        self._allocation: dict[ConfiguredVerifier, tuple[int, int, int]] = {}
        if self._n_cpu:
            cpu_left = self._n_cpu
        else:
            cpu_left = cpu_count()
        if self._n_gpu:
            gpu_left = self._n_gpu
        else:
            gpu_left = nvidia_gpu_count()

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
                curr_gpu = gpu_left - 1
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
        out_csv: Path | None = None,
        vnncompat: bool = False,
        benchmark: str | None = None,
    ) -> _VbsResult:
        """Evaluate the PF in vbs mode.

        Arguments:
            instances: Instances to evaluate.
            out_csv: File where the results are written to.
            vnncompat: Use some compat kwargs.
            benchmark: Only if vnncompat, benchmark name.
        """
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

                if out_csv:
                    self._csv_log_result(
                        out_csv,
                        result,
                        instance,
                        cv.verifier,
                        cv.configuration,
                    )

        return self._vbs_from_cost_dict(results)

    @staticmethod
    def _csv_log_result(
        out_csv: Path,
        result: CompleteVerificationResult,
        instance: VerificationInstance,
        verifier: str,
        configuration: Configuration,
    ):
        if isinstance(result, Ok):
            res_d = result.unwrap()
            success = "OK"
        elif isinstance(result, Err):
            res_d = result.unwrap_err()
            success = "ERR"

        inst_d = {
            "network": instance.network,
            "property": instance.property,
            "timeout": instance.timeout,
            "verifier": verifier,
            "config": configuration,
            "success": success,
        }

        if not out_csv.exists():
            init_verification_result_csv(out_csv)

        vdr = VerificationDataResult.from_verification_result(res_d, inst_d)
        csv_append_verification_result(vdr, out_csv)

    @staticmethod
    def _vbs_from_cost_dict(cost_dict: _CostDict) -> _VbsResult:
        vbs: _VbsResult = {}

        for cv, instance_costs in cost_dict.items():
            for instance, cost in instance_costs.items():
                str_inst = str(instance)

                if str_inst not in vbs:
                    vbs[str_inst] = (cost, cv.verifier)
                    continue

                if cost < vbs[str_inst][0]:
                    vbs[str_inst] = (cost, cv.verifier)

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

    # TODO: Arg types
    def _get_verifiers(
        self,
        instance,
        vnncompat,
        benchmark,
        verifier_kwargs,
    ) -> dict[ConfiguredVerifier, CompleteVerifier]:
        verifiers: dict[ConfiguredVerifier, CompleteVerifier] = {}

        for cv in self._portfolio:
            v = _get_verifier(
                instance,
                cv,
                vnncompat,
                benchmark,
                verifier_kwargs,
                self._allocation,
            )
            assert isinstance(v, CompleteVerifier)
            verifiers[cv] = v

        return verifiers

    def verify_instances(
        self,
        instances: Iterable[VerificationInstance],
        *,
        out_csv: Path | None = None,
        vnncompat: bool = False,
        benchmark: str | None = None,
        verifier_kwargs: dict[str, dict[str, Any]] | None = None,
        uses_simplified_network: Iterable[str] | None = None,
    ) -> dict[VerificationInstance, VerificationDataResult]:
        """Run the PF in parallel.

        Arguments:
            instances: Instances to evaluate.
            out_csv: File where the results are written to.
            vnncompat: Use some compat kwargs.
            benchmark: Only if vnncompat, benchmark name.
            verifier_kwargs: Kwargs passed to verifiers.
            uses_simplified_network: Have some verifiers use simplified nets.
        """
        if self._vbs_mode:
            raise RuntimeError("Function not compatible with vbs_mode")

        if out_csv:
            out_csv = out_csv.expanduser().resolve()

        results: dict[VerificationInstance, VerificationDataResult] = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for instance in instances:
                logger.info(f"Running portfolio on {str(instance)}")

                futures: dict[
                    Future[CompleteVerificationResult], ConfiguredVerifier
                ] = {}
                self._verifiers = self._get_verifiers(
                    instance,
                    vnncompat,
                    benchmark,
                    verifier_kwargs,
                )
                is_solved = False

                for cv in self._portfolio:
                    if (
                        uses_simplified_network
                        and cv.verifier in uses_simplified_network
                    ):
                        target_instance = instance.as_simplified_network()
                    else:
                        target_instance = instance

                    future = executor.submit(
                        self._verifiers[cv].verify_instance, 
                        target_instance,
                        config=cv.configuration
                    )
                    futures[future] = cv

                for future in concurrent.futures.as_completed(futures):
                    fut_cv = futures[future]
                    result = future.result()

                    if not is_solved:
                        got_solved = self._process_result(
                            result, results, fut_cv, instance, self._verifiers
                        )

                        if got_solved and not is_solved:
                            is_solved = True

                        if out_csv:
                            self._csv_log_result(
                                out_csv,
                                result,
                                instance,
                                fut_cv.verifier,
                                fut_cv.configuration,
                            )

        return results

    def _process_result(
        self,
        result: CompleteVerificationResult,
        results: dict[VerificationInstance, VerificationDataResult],
        cv: ConfiguredVerifier,
        instance: VerificationInstance,
        verifiers: dict[ConfiguredVerifier, CompleteVerifier],
    ) -> bool:
        instance_data: dict[str, Any] = {
            "network": instance.network,
            "property": instance.property,
            "timeout": instance.timeout,
            "verifier": cv.verifier,
            "config": cv.configuration,
        }

        if isinstance(result, Ok):
            r = result.unwrap()

            if r.result == "TIMEOUT":
                log_string = f"{cv.verifier} timed out"
            else:
                self._cancel_running(cv, verifiers)
                log_string = (
                    f"Verified by {cv.verifier} in {r.took:.2f} sec, "
                    f"result = {r.result}"
                )

            instance_data["success"] = "OK"
            results[instance] = VerificationDataResult.from_verification_result(
                r, instance_data
            )

            # Signal that the instance was solved
            if r.result in ["SAT", "UNSAT"]:
                logger.info(log_string)
                return True
        elif isinstance(result, Err):
            log_string = f"{cv.verifier} errored."
            r = result.unwrap_err()

            instance_data["success"] = "ERR"
            results[instance] = VerificationDataResult.from_verification_result(
                r, instance_data
            )

        logger.info(log_string)
        # Instance was not solved
        return False

    def _cancel_running(
        self,
        first_cv: ConfiguredVerifier,
        verifiers: dict[ConfiguredVerifier, CompleteVerifier],
    ):
        others = set_iter_except(self._portfolio.get_set(), first_cv)
        for other_cv in others:
            verifiers[other_cv].set_timeout_event()

    def _cleanup(self):
        """Kill all running verifiers processes."""
        if not self._verifiers:
            sys.exit(0)

        for verifier_inst in self._verifiers.values():
            try:
                verifier_inst.set_timeout_event()
            finally:
                pass

        sys.exit(0)
