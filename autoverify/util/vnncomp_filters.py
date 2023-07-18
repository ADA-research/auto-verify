"""_summary_."""
from typing import Callable

from autoverify.util.instances import VerificationInstance

filters: dict[str, Callable[[VerificationInstance], bool]] = {
    "mnist_small": lambda vi: vi.network.name.endswith("2.onnx"),
    "mnist_medium": lambda vi: vi.network.name.endswith("4.onnx"),
    "mnist_large": lambda vi: vi.network.name.endswith("6.onnx"),
}
