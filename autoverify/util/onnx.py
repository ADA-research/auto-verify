from pathlib import Path

import onnxruntime


# TODO: Is a flat array always returned?
def get_input_shape(onnx_file: Path) -> list[int]:
    """_summary_."""
    model = onnxruntime.InferenceSession(
        str(onnx_file),
        providers=["CPUExecutionProvider"],
    )

    return model.get_inputs()[0].shape
