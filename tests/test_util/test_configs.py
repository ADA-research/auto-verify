from pathlib import Path

import pytest
from ConfigSpace import ConfigurationSpace

from autoverify.util.configs import (
    config_dict_from_config_str,
    config_from_str,
    config_from_txt_file,
)


@pytest.fixture
def config_str() -> str:
    return """Configuration(values={
    'A': 500,
    'B': 5.0,
    'C': True,
    })"""


def test_config_dict_from_config_str(config_str: str):
    assert config_dict_from_config_str(config_str) == {
        "A": 500,
        "B": 5.0,
        "C": True,
    }


def test_config_from_str(
    config_str: str, simple_configspace: ConfigurationSpace
):
    assert (
        config_from_str(config_str, simple_configspace)
        == simple_configspace.get_default_configuration()
    )


def test_config_from_txt_file(
    tmp_path: Path, config_str: str, simple_configspace: ConfigurationSpace
):
    temp_file = tmp_path / "tmp_cfg.txt"
    temp_file.write_text(config_str)

    assert (
        config_from_txt_file(temp_file, simple_configspace)
        == simple_configspace.get_default_configuration()
    )
