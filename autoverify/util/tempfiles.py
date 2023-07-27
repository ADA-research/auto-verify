"""YAML file utils."""
# TODO: Clean up the tempfiles. Currently it will fill up storage until shutdown
import csv
import json
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import IO, Any, Iterable

import yaml

from autoverify.util.instances import VerificationInstance


def tmp_file(extension: str) -> IO[str]:
    """Return a new tempfile with the given extension."""
    return tempfile.NamedTemporaryFile("w", suffix=extension, delete=False)


# TODO: Just make a function that returns a tempfile with extension as param
def tmp_json_file() -> IO[str]:
    """Returns a new temporary named empty yaml file."""
    return tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)


def tmp_json_file_from_dict(a_dict: dict[Any, Any]) -> IO[str]:
    """Returns a new temporary named json file with the dict written to it."""
    tmp_json = tmp_json_file()

    with open(tmp_json.name, "w") as fp:
        json.dump(a_dict, fp)

    return tmp_json


def tmp_yaml_file() -> IO[str]:
    """Returns a new temporary named empty yaml file."""
    return tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False)


def tmp_yaml_file_from_dict(a_dict: dict[Any, Any]) -> IO[str]:
    """Returns a new temporary named yaml file with the dict written to it."""
    tmp_yaml = tmp_yaml_file()
    yaml.dump(a_dict, tmp_yaml)

    return tmp_yaml


@contextmanager
def tmp_instances_csv(instances: Iterable[VerificationInstance]):
    tmp_csv = tempfile.NamedTemporaryFile("r", suffix=".csv", delete=False)

    with open(tmp_csv.name, "w") as f:
        writer = csv.writer(f, delimiter=",")

        for inst in instances:
            writer.writerow(inst.as_row())

    try:
        yield tmp_csv
    finally:
        Path(tmp_csv.name).unlink()

    return tmp_csv
