"""Onnx utility functions."""
from pathlib import Path

import onnx
import onnxruntime


# FIXME: This is not always an array of ints
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


def get_input_ouput_names(onnx_path: Path) -> tuple[list[str], list[str]]:
    """Get the input and output layer node names."""
    model = onnx.load(str(onnx_path))
    output = [node.name for node in model.graph.output]

    input_all = [node.name for node in model.graph.input]
    input_initializer = [node.name for node in model.graph.initializer]
    net_feed_input = list(set(input_all) - set(input_initializer))

    return net_feed_input, output
