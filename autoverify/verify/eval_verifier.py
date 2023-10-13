"""Evaluate the performance of a verifier on a set of instances.

This file is meant for functions that benchmark the performance of a verifier,
collecting detailed results about the verification run.
"""
import copy
import logging
from pathlib import Path

from ConfigSpace import Configuration
from result import Err, Ok

from autoverify.util.instances import (
    VerificationDataResult,
    csv_append_verification_result,
    init_verification_result_csv,
    read_vnncomp_instances,
)
from autoverify.util.verification_instance import VerificationInstance
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp import (
    inst_bench_to_verifier,
    inst_bench_verifier_config,
)
from autoverify.verifier import Nnenum
from autoverify.verifier.verifier import CompleteVerifier

logger = logging.getLogger(__name__)


def _warmup(
    verifier: CompleteVerifier | str,
    instance: VerificationInstance,
    config: Configuration | Path | None,
):
    logger.info("Starting warmup run")
    warmup_inst = copy.deepcopy(instance)

    if isinstance(verifier, str):
        v = verifier_from_name(verifier)()
        assert isinstance(v, CompleteVerifier)
        v.verify_property(
            warmup_inst.network, warmup_inst.property, config=config, timeout=10
        )
    else:
        verifier.verify_property(
            warmup_inst.network,
            warmup_inst.property,
            config=config,
            timeout=10,
        )

    logger.info("Finished warmup run")


def eval_instance(
    verifier: CompleteVerifier,
    instance: VerificationInstance,
    *,
    config: Configuration | Path | None = None,
) -> VerificationDataResult:
    """_summary_."""
    logger.info(
        f"\nVerifying property {instance.property.name} on "
        f"{instance.network.name} with verifier {verifier.name} and "
        f"configuration {config or 'default'} "
        f"(timeout = {instance.timeout} sec.)"
    )

    static_data = (
        instance.network.name,
        instance.property.name,
        instance.timeout,
        verifier.name,
        str(config),
    )

    result = verifier.verify_instance(instance, config=config)

    if isinstance(result, Ok):
        logger.info("Verification finished succesfully.")
        unwrap_result = result.unwrap()
        logger.info(f"Result: {unwrap_result.result}")

        return VerificationDataResult(
            *static_data,
            "OK",
            unwrap_result.result,
            unwrap_result.took,
            unwrap_result.counter_example,
            unwrap_result.err,
            unwrap_result.stdout,
        )
    elif isinstance(result, Err):
        unwrap_result = result.unwrap_err()
        logger.info("Exception during verification.")
        logger.info(result.err)

        return VerificationDataResult(
            *static_data,
            "ERR",
            unwrap_result.result,
            unwrap_result.took,
            None,
            unwrap_result.err,
            unwrap_result.stdout,
        )

    raise RuntimeError("Result should be Ok | Err")


# TODO: make vnncompat a param for `eval_verifier`
# that probably means the `verifier` param needs to become a `str`
# or maybe make it a param in one of the other functions
def eval_verifier_vnncompat(
    verifier: str,
    benchmark: str,
    instances: list[VerificationInstance],
    config: Configuration | Path | None,
    *,
    warmup: bool = True,
    output_csv_path: Path | None = None,
) -> dict[VerificationInstance, VerificationDataResult]:
    """_summary_."""
    results: dict[VerificationInstance, VerificationDataResult] = {}

    if output_csv_path is not None:
        init_verification_result_csv(output_csv_path)

    if warmup:
        _warmup(verifier, instances[0], config)

    for instance in instances:
        verifier_inst = inst_bench_to_verifier(benchmark, instance, verifier)
        result = eval_instance(verifier_inst, instance, config=config)
        results[instance] = result

        logger.info(f"Verification took {result.took} seconds.")

        if output_csv_path is not None:
            csv_append_verification_result(result, output_csv_path)

    return results


def eval_verifier(
    verifier: CompleteVerifier,
    instances: list[VerificationInstance],
    config: Configuration | Path | None,
    *,
    warmup: bool = True,
    use_simplified_network: bool = False,
    output_csv_path: Path | None = None,
) -> dict[VerificationInstance, VerificationDataResult]:
    """_summary_."""
    results: dict[VerificationInstance, VerificationDataResult] = {}

    if output_csv_path is not None:
        init_verification_result_csv(output_csv_path)

    if use_simplified_network:
        for i, instance in enumerate(instances):
            instances[i] = instance.as_simplified_network()

    if warmup:
        _warmup(verifier, instances[0], config)

    for instance in instances:
        result = eval_instance(verifier, instance, config=config)
        results[instance] = result

        logger.info(f"Verification took {result.took} seconds.")

        if output_csv_path is not None:
            csv_append_verification_result(result, output_csv_path)

    return results


def eval_vnn_default(
    verifier: str,
    benchmark: str,
    vnncomp_path: Path,
    output_csv_path: Path,
    *,
    warmup: bool = True,
) -> dict[VerificationInstance, VerificationDataResult]:
    """_summary_."""
    results: dict[VerificationInstance, VerificationDataResult] = {}
    instances = read_vnncomp_instances(benchmark, vnncomp_path)

    if output_csv_path is not None:
        init_verification_result_csv(output_csv_path)

    if warmup:
        _warmup(verifier, instances[0], None)

    for inst in instances:
        verifier_inst = inst_bench_to_verifier(benchmark, inst, verifier)

        assert isinstance(verifier_inst, CompleteVerifier)
        result = eval_instance(verifier_inst, inst)

        logger.info(f"Verification took {result.took} seconds.")

        if output_csv_path is not None:
            csv_append_verification_result(result, output_csv_path)

    return results


def eval_vnn_verifier(
    verifier: str,
    benchmark: str,
    vnncomp_path: Path,
    output_csv_path: Path,
    configs_dir: Path,
    *,
    warmup: bool = True,
) -> dict[VerificationInstance, VerificationDataResult]:
    """_summary_."""
    results: dict[VerificationInstance, VerificationDataResult] = {}
    instances = read_vnncomp_instances(benchmark, vnncomp_path)

    if output_csv_path is not None:
        init_verification_result_csv(output_csv_path)

    if warmup:
        _warmup(verifier, instances[0], None)

    for inst in instances:
        cfg = inst_bench_verifier_config(benchmark, inst, verifier, configs_dir)
        # HACK:
        if verifier == "verinet":
            verifier_inst = inst_bench_to_verifier(benchmark, inst, "verinet")
        elif verifier == "nnenum":
            verifier_inst = Nnenum(use_auto_settings=True)
        else:
            verifier_t = verifier_from_name(verifier)()
            assert isinstance(verifier_t, CompleteVerifier)
            verifier_inst = verifier_t

        assert isinstance(verifier_inst, CompleteVerifier)
        result = eval_instance(verifier_inst, inst, config=cfg)

        logger.info(f"Verification took {result.took} seconds.")

        if output_csv_path is not None:
            csv_append_verification_result(result, output_csv_path)

    return results
