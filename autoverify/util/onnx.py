"""Onnx utility functions."""
from pathlib import Path

import onnxruntime


# TODO: Is a flat array always returned from `model.get_inputs()[0].shape`?
def get_input_shape(onnx_file: Path) -> list[int]:
    """Get the input shape of a network that is saved as an onnx file.

    Args:
        onnx_file: The onnx file to get the input shape from.

    Returns:
        list[int]: The input shape of the network.
    """
    model = onnxruntime.InferenceSession(str(onnx_file))

    # Convert to explicit flat int array for mypy
    input_shape: list[int] = model.get_inputs()[0].shape
    return input_shape
