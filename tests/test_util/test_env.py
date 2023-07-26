# TODO: Find a way to test `pkill_match(es)`
import os
import sys
from pathlib import Path

from autoverify.util.env import (
    copy_env_file_to,
    cwd,
    environment,
    exit_functions,
    get_file_path,
    sys_path,
)


# NOTE: Theres no reason for `get_file_path` to actually exist, since
# `Path().resolve().parent` does the same thing
def test_get_file_path():
    assert get_file_path(Path(__file__)) == Path(__file__).resolve().parent


def test_copy_env_file_to(tmp_path: Path):
    tmp_yaml = tmp_path / "environment.yml"
    tmp_yaml.touch()

    tmp_install_dir = tmp_path / "tool/"
    tmp_install_dir.mkdir()

    copy_env_file_to(tmp_yaml, tmp_install_dir)

    new_yaml = tmp_install_dir / "environment.yml"
    assert new_yaml.is_file()
    assert new_yaml.name == "environment.yml"


def test_environment_context_manager():
    original_var = os.getenv("MY_ENV_VAR")
    expected_value = "TEST_VALUE"

    with environment(MY_ENV_VAR=expected_value):
        assert os.getenv("MY_ENV_VAR") == expected_value

    assert os.getenv("MY_ENV_VAR") == original_var


def test_cwd_context_manager(tmp_path: Path):
    original_wd = os.getcwd()

    with cwd(tmp_path):
        assert os.getcwd() == str(tmp_path)

    assert os.getcwd() == original_wd


def test_sys_path_context_manager(tmp_path: Path):
    with sys_path(tmp_path):
        assert sys.path[0] == str(tmp_path)

    assert str(tmp_path) not in sys.path


def test_exit_functions_context_manager():
    value = 10
    result = [0]

    def cleanup_function():
        result[0] = value

    with exit_functions([cleanup_function]):
        pass

    assert result[0] == value
