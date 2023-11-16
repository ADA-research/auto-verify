"""YAML file utils."""
import atexit
import json
import tempfile
from pathlib import Path
from typing import IO, Any

import yaml

_tempfiles_to_clean: list[str] = []


def _reg_for_clean(f: str | Path):
    _tempfiles_to_clean.append(str(f))


@atexit.register
def _cleanup_tempfiles():  # pragma: no cover
    for f in _tempfiles_to_clean:
        p = Path(f)
        if p.exists() and p.is_file():
            p.unlink()


def tmp_file(extension: str) -> IO[str]:
    """Return a new tempfile with the given extension."""
    f = tempfile.NamedTemporaryFile("w", suffix=extension, delete=False)
    _reg_for_clean(f.name)
    return f


# TODO: Just make a function that returns a tempfile with extension as param
def tmp_json_file() -> IO[str]:
    """Returns a new temporary named empty yaml file."""
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    _reg_for_clean(f.name)
    return f


def tmp_json_file_from_dict(a_dict: dict[Any, Any]) -> IO[str]:
    """Returns a new temporary named json file with the dict written to it."""
    tmp_json = tmp_json_file()

    with open(tmp_json.name, "w") as fp:
        json.dump(a_dict, fp)

    return tmp_json


def tmp_yaml_file() -> IO[str]:
    """Returns a new temporary named empty yaml file."""
    f = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False)
    _reg_for_clean(f.name)
    return f


def tmp_yaml_file_from_dict(a_dict: dict[Any, Any]) -> IO[str]:
    """Returns a new temporary named yaml file with the dict written to it."""
    tmp_yaml = tmp_yaml_file()
    yaml.dump(a_dict, tmp_yaml)

    return tmp_yaml
