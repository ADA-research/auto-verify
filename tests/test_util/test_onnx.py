from pathlib import Path

import pytest

from autoverify.util.instances import VerificationInstance
from autoverify.util.onnx import get_input_ouput_names, get_input_shape


@pytest.fixture
def networks(trivial_sat, trivial_unsat, trivial_nano) -> list[Path]:
    return [
        trivial_sat.network,
        trivial_unsat.network,
        trivial_nano.network,
    ]


def test_get_input_shape(networks: list[Path]):
    assert get_input_shape(networks[0]) == [1, 1, 1, 5]
    assert get_input_shape(networks[1]) == [1, 1, 1, 5]
    assert get_input_shape(networks[2]) == [1]


def test_get_input_output_names(networks: list[Path]):
    assert get_input_ouput_names(networks[0]) == (["input"], ["linear_7_Add"])
    assert get_input_ouput_names(networks[2]) == (["model_in"], ["model_out"])
