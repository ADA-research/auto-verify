"""Verifier VNNCOMP compatability.

Return verifier instances that should be compatible with the given
benchmark + instance.
"""
from pathlib import Path
from typing import Any

from ConfigSpace import Configuration

from autoverify.util.verification_instance import VerificationInstance
from autoverify.util.verifiers import verifier_from_name
from autoverify.verifier import Verinet
from autoverify.verifier.verifier import CompleteVerifier


# HACK:
def inst_bench_to_kwargs(
    benchmark: str,
    verifier: str,
    instance: VerificationInstance,
) -> dict[str, Any]:
    """Get the kwargs for a benchmark."""
    if verifier == "nnenum":
        return {"use_auto_settings": True}
    elif verifier == "abcrown":  # TODO: All benchmarks
        if benchmark == "acasxu":
            return {"yaml_override": {"data__num_outputs": 5}}
        elif benchmark.startswith("sri_resnet_"):
            return {
                "yaml_override": {
                    "model__onnx_quirks": "{'Reshape': {'fix_batch_size': True}}"  # noqa: E501
                }
            }
        return {}
    elif verifier == "ovalbab":
        return {}
    elif verifier == "verinet":
        if benchmark == "acasxu":
            return {"transpose_matmul_weights": True}
        elif benchmark == "cifar2020":
            if instance.network.name.find("convBigRELU") >= 0:
                return {"dnnv_simplify": True}
        elif benchmark == "cifar100_tinyimagenet_resnet":
            return {"dnnv_simplify": True}
        elif benchmark == "nn4sys":
            if instance.network.name == "lindex.onnx":
                return {"dnnv_simplify": True}
        return {}

    raise ValueError("Invalid verifier")


def inst_bench_to_verifier(
    benchmark: str,
    instance: VerificationInstance,
    verifier: str,
    allocation: tuple[int, int, int] | None = None,
) -> CompleteVerifier:
    """Get an instantiated verifier."""
    verifier_inst = verifier_from_name(verifier)(
        **inst_bench_to_kwargs(benchmark, verifier, instance),
        cpu_gpu_allocation=allocation,
    )
    assert isinstance(verifier_inst, CompleteVerifier)
    return verifier_inst


def _get_abcrown_config(benchmark: str, instance: VerificationInstance) -> str:
    net_name = instance.network.name

    if benchmark == "acasxu":
        return "acasxu.yaml"
    elif benchmark == "carvana_unet":
        if net_name == "unet_simp_small.onnx":
            return "carvana-unet-simp.yaml"
        elif net_name == "unet_upsample_small.onnx":
            return "carvana-unet-upsample.yaml"
        raise ValueError(f"Couldnt find config for {instance.as_row()}")
    elif benchmark == "cifar100_tinyimagenet_resnet":
        if net_name == "CIFAR100_resnet_small.onnx":
            return "cifar100_small_2022.yaml"
        elif net_name == "CIFAR100_resnet_medium.onnx":
            return "cifar100_med_2022.yaml"
        elif net_name == "CIFAR100_resnet_large.onnx":
            return "cifar100_large_2022.yaml"
        elif net_name == "CIFAR100_resnet_super.onnx":
            return "cifar100_super_2022.yaml"
        elif net_name == "TinyImageNet_resnet_medium.onnx":
            return "tinyimagenet_2022.yaml"
        raise ValueError(f"Couldnt find config for {instance.as_row()}")
    elif benchmark == "cifar2020":
        return "cifar2020_2_255.yaml"
    elif benchmark == "cifar_biasfield":
        return "cifar_biasfield.yaml"
    elif benchmark == "mnist_fc":
        if net_name == "mnist-net_256x2.onnx":
            return "mnistfc_small.yaml"
        elif (
            net_name == "mnist-net_256x4.onnx"
            or net_name == "mnist-net_256x6.onnx"
        ):
            return "mnistfc.yaml"
        raise ValueError(f"Couldnt find config for {instance.as_row()}")
    elif benchmark == "nn4sys":
        if net_name == "lindex_deep.onnx" or net_name == "lindex.onnx":
            return "nn4sys_2022_lindex.yaml"
        elif net_name == "mscn_128d_dual.onnx" or net_name == "mscn_128d.onnx":
            return "nn4sys_2022_128d.yaml"
        elif net_name == "mscn_2048d.onnx":
            return "nn4sys_2022_2048d.yaml"
        raise ValueError(f"Couldnt find config for {instance.as_row()}")
    elif benchmark == "oval21":
        return "oval22.yaml"
    elif benchmark == "sri_resnet_a":
        return "resnet_A.yaml"
    elif benchmark == "sri_resnet_b":
        return "resnet_B.yaml"
    elif benchmark == "vggnet16":
        return "vggnet16.yaml"

    raise ValueError(f"Couldnt find config for {instance.as_row()}")


def _get_ovalbab_config(benchmark: str) -> str | None:
    # Oval-BaB did not participate in VNNCOMP2022, so do the best we can with
    # configs from VNNCOMP2021.
    if benchmark in ["acasxu", "cifar2020", "mnist_fc", "nn4sys", "oval21"]:
        if benchmark == "mnist_fc":
            return "mnistfc_vnncomp21.json"

        return benchmark + "_vnncomp21.json"

    return None


def _get_verinet_config(benchmark: str) -> Configuration:
    # VeriNet's entry in the VNNCOMP2022 is not public, so do the best we can
    # with configs from VNNCOMP2021
    default_cfg = Verinet().default_config

    if benchmark in ["acasxu", "mnist_fc"]:
        default_cfg["NUM_ITER_OPTIMISED_RELAXATIONS"] = 1
        default_cfg["INDIRECT_HIDDEN_MULTIPLIER"] = 0.75
        default_cfg["INDIRECT_INPUT_MULTIPLIER"] = 0.75
        return default_cfg
    elif benchmark == "cifar2020":
        default_cfg["NUM_ITER_OPTIMISED_RELAXATIONS"] = 3
        default_cfg["INDIRECT_HIDDEN_MULTIPLIER"] = 0.5
        default_cfg["INDIRECT_INPUT_MULTIPLIER"] = 0.75
        return default_cfg

    return default_cfg


def inst_bench_verifier_config(
    benchmark: str,
    instance: VerificationInstance,
    verifier: str,
    configs_dir: Path,
) -> Configuration | Path | None:
    """Return the verifier and the VNNCOMP config."""
    if benchmark == "test_props":
        return None

    if verifier == "nnenum":
        return None
    elif verifier == "abcrown":
        cfg_file = _get_abcrown_config(benchmark, instance)
        return Path(configs_dir / "abcrown" / cfg_file)
    elif verifier == "ovalbab":
        cfg = _get_ovalbab_config(benchmark)
        if cfg is not None:
            return Path(configs_dir / "ovalbab" / cfg)
        return cfg
    elif verifier == "verinet":
        return _get_verinet_config(benchmark)

    raise ValueError("Invalid verifier")
