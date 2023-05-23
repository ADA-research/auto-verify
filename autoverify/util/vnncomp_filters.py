"""_summary_."""
from autoverify.util.instances import VerificationInstance


def mnist_small_filter(inst: VerificationInstance) -> bool:
    """Small mnist instances end with 2.onnx."""
    return inst.network.name.endswith("2.onnx")


def mnist_medium_filter(inst: VerificationInstance) -> bool:
    """_summary_."""
    return inst.network.name.endswith("4.onnx")
