"""Conda utility functions."""

import shlex
import subprocess
from pathlib import Path

AV_ENV_BASE_NAME = "__av__"


def is_conda_installed() -> bool:
    """Checks if conda is installed.

    Returns:
        bool: True if conda is installed, False otherwise.
    """
    cmd = shlex.split("conda --version")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        return False

    return True


def delete_conda_env(env_name: str):
    """Deletes a conda environment with the given name.

    Args:
        env_name: The name of the environment to be deleted.
    """
    cmd = shlex.split(f"conda remove -n {env_name} --all -y")
    subprocess.run(cmd, check=True, capture_output=True)


def create_env_from_file(file: Path):
    """Creates a new conda environment from a file.

    Args:
        file: The file to create the environment from, should be a yaml file
    """
    cmd = shlex.split(f"conda env create -f {str(file)}")
    subprocess.run(cmd, check=True, capture_output=True)


def get_av_conda_envs() -> list[str]:
    """Return a list of conda environments used by auto-verify."""
    conda_envs: list[str] = []

    cmd = shlex.split("conda env list")
    result = subprocess.run(cmd, check=True, capture_output=True)

    for line in str(result.stdout.decode("utf-8")).splitlines()[2:-1]:
        env_name = line.split(maxsplit=1)[0]

        if env_name.find(AV_ENV_BASE_NAME) == 0:
            conda_envs.append(env_name)

    return conda_envs


def get_verifier_conda_env_name(verifier: str) -> str:
    """Returns the conda environment name for the verifier, if it exists.

    Args:
        verifier: The verifier to get the conda env name for.

    Returns:
        str | None: conda environment name, if it exists.
    """
    # TODO: Check for if this env actually exists
    return AV_ENV_BASE_NAME + verifier


def get_conda_path() -> Path:
    """Returns the Conda path."""
    base_env = get_field_from_conda_info("base environment")

    if isinstance(base_env, str):
        base_env = base_env.split(" ", maxsplit=1)[0]
        return Path(base_env)

    # TODO: Handle exception properly
    raise Exception(f"Could not fetch conda base environment info: {base_env}")


def get_conda_info() -> str:
    """Returns the output of `conda info`."""
    cmd = shlex.split("conda info")
    result = subprocess.run(cmd, check=True, capture_output=True)

    return result.stdout.decode()


# TODO: Support for the multi line fields
def get_field_from_conda_info(field: str) -> str | list[str] | None:
    """_summary_."""
    conda_info = get_conda_info()

    for line in conda_info.splitlines():
        key_value = line.split(" : ", maxsplit=1)

        if key_value[0] == "":
            continue

        if len(key_value) == 2:
            key, value = key_value

            if key.strip() == field:
                return value

    return None


def get_conda_source_cmd(conda_path: Path) -> list[str]:
    """_summary_."""
    return shlex.split(
        f"source {str(conda_path / 'etc' / 'profile.d' / 'conda.sh')}"
    )
