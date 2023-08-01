"""Verifier VNNCOMP compatability.

Return verifier instances that should be compatible with the given 
benchmark + instance."""
from pathlib import Path

from ConfigSpace import Configuration

from autoverify.util.verification_instance import VerificationInstance
from autoverify.verifier import AbCrown, Nnenum, OvalBab, Verinet
from autoverify.verifier.verifier import CompleteVerifier


def inst_bench_to_verifier(
    benchmark: str, instance: VerificationInstance, verifier: str
) -> CompleteVerifier:
    """_summary_."""
    if verifier == "nnenum":
        return Nnenum()
    elif verifier == "abcrown":
        if benchmark == "acasxu":
            return AbCrown(yaml_override={"data__num_outputs": 5})
        elif benchmark.startswith("sri_resnet_"):
            return AbCrown(
                yaml_override={
                    "model__onnx_quirks": "{'Reshape': {'fix_batch_size': True}}"  # noqa: E501
                }
            )
        return AbCrown()
    elif verifier == "ovalbab":
        return OvalBab()
    elif verifier == "verinet":
        if benchmark == "acasxu":
            return Verinet(transpose_matmul_weights=True)
        elif benchmark == "cifar202":
            if instance.network.name.find("convBigRELU") >= 0:
                return Verinet(dnnv_simplify=True)
        elif benchmark == "cifar100_tinyimagenet_resnet":
            return Verinet(dnnv_simplify=True)

        return Verinet()

    raise ValueError("Invalid verifier")


def inst_bench_verifier_config(
    benchmark: str,
    instance: VerificationInstance,
    verifier: str,
) -> Configuration | None:
    """Return the verifier and the VNNCOMP config."""
    # if verifier == "nnenum":
    #     return None
    # elif verifier == "abcrown":
    #     pass
    # elif verifier == "ovalbab":
    #     pass
    # elif verifier == "verinet":
    #     pass
    # raise ValueError("Invalid verifier")
    raise NotImplementedError
