"""_summary_."""
from typing import Callable

from autoverify.util.verification_instance import VerificationInstance

filters: dict[str, Callable[[VerificationInstance], bool]] = {
    "mnist_small": lambda vi: vi.network.name.endswith("2.onnx"),
    "mnist_medium": lambda vi: vi.network.name.endswith("4.onnx"),
    "mnist_large": lambda vi: vi.network.name.endswith("6.onnx"),
    "cifar_base": lambda vi: vi.network.name.endswith("base_kw.onnx"),
    "cifar_deep": lambda vi: vi.network.name.endswith("deep_kw.onnx"),
    "cifar_wide": lambda vi: vi.network.name.endswith("wide_kw.onnx"),
}
