"""_summary_."""
from __future__ import annotations

import csv
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, overload

import pandas as pd

from autoverify.util.dataclass import get_dataclass_field_names
from autoverify.util.verification_instance import VerificationInstance
from autoverify.verifier.verification_result import VerificationResultString


@dataclass
class VerificationDataResult:
    """_summary_."""

    network: str
    property: str
    timeout: int | None
    verifier: str
    config: str
    success: Literal["OK", "ERR"]
    result: VerificationResultString
    took: float
    counter_example: str | tuple[str, str] | None
    stderr: str | None
    stdout: str | None

    def __post_init__(self):
        """_summary_."""
        if self.config == "None":
            self.config = "default"

    def as_csv_row(self) -> list[str]:
        """Convert data to a csv row writeable."""
        if isinstance(self.counter_example, tuple):
            self.counter_example = "\n".join(self.counter_example)

        return [
            self.network,
            self.property,
            str(self.timeout),
            self.verifier,
            self.config,
            self.success,
            self.result,
            str(self.took),
            self.counter_example or "",
            self.stderr or "",
            self.stdout or "",
        ]


def init_verification_result_csv(csv_path: Path):
    """_summary_."""
    with open(str(csv_path.expanduser()), "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(get_dataclass_field_names(VerificationDataResult))


def csv_append_verification_result(
    verification_result: VerificationDataResult, csv_path: Path
):
    """_summary_."""
    with open(str(csv_path.expanduser()), "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(verification_result.as_csv_row())


def read_verification_result_from_csv(
    csv_path: Path,
) -> list[VerificationDataResult]:
    """Reads a verification results csv to a list of its dataclass."""
    results_df = pd.read_csv(csv_path)
    verification_results: list[VerificationDataResult] = []

    for _, row in results_df.iterrows():
        row = row.to_list()
        verification_results.append(VerificationDataResult(*row))

    return verification_results


def write_verification_results_to_csv(results: pd.DataFrame, csv_path: Path):
    """Writes a verification results df to a csv."""
    results.to_csv(csv_path, index=False)


def verification_instances_to_smac_instances(
    instances: Sequence[VerificationInstance],
) -> list[str]:
    """Convert a list of `VerificationInstace` objects to SMAC instances.

    See the `as_smac_instance` docstring of the `VerificationInstance` class for
    more details.

    Args:
        instances: The list of `VerificationInstance` objects to convert.

    Returns:
        list[str]: The SMAC instance strings.
    """
    return [inst.as_smac_instance() for inst in instances]


@overload
def read_vnncomp_instances(  # type: ignore
    benchmark: str,
    vnncomp_path: Path,
    *,
    predicate: Callable[[VerificationInstance], bool] | None = None,
    as_smac: Literal[False] = False,
    resolve_paths: bool = False,
) -> list[VerificationInstance]:
    ...


@overload
def read_vnncomp_instances(
    benchmark: str,
    vnncomp_path: Path,
    *,
    predicate: Callable[[VerificationInstance], bool] | None = None,
    as_smac: Literal[True] = True,
    resolve_paths: bool = False,
) -> list[str]:
    ...


def read_vnncomp_instances(
    benchmark: str,
    vnncomp_path: Path,
    *,
    predicate: Callable[[VerificationInstance], bool] | None = None,
    as_smac: bool = False,
    resolve_paths: bool = False,
) -> list[VerificationInstance] | list[str]:
    """Read the instances of a VNNCOMP benchmark.

    Reads the CSV file of a VNNCOMP benchmark, parsing the network, property and
    timeout values.

    Args:
        benchmark: The name of the benchmark directory.
        vnncomp_path: The path to the VNNCOMP benchmark directory
        predicate: A function that, given a `VerificationInstance` returns
            either True or False. If False is returned, the
            `VerificationInstance` is dropped from the returned instances.
        as_smac: Return the instances as smac instance strings.

    Returns:
        list[VerificationInstance] | list[str]: A list of
            `VerificationInstance` or string objects
            that hold the network, property and timeout.
    """
    if not vnncomp_path.is_dir():
        raise ValueError("Could not find VNNCOMP directory")

    benchmark_dir = vnncomp_path / benchmark

    if not benchmark_dir.is_dir():
        raise ValueError(
            f"{benchmark} is not a valid benchmark in {str(vnncomp_path)}"
        )

    instances = benchmark_dir / "instances.csv"

    verification_instances = []

    with open(str(instances)) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            network, property, timeout = row

            net_path = Path(str(benchmark_dir / network))
            prop_path = Path(str(benchmark_dir / property))

            instance = VerificationInstance(
                net_path if not resolve_paths else net_path.resolve(),
                prop_path if not resolve_paths else prop_path.resolve(),
                int(float(timeout)),  # FIXME: Timeouts can be floats
            )

            if predicate and not predicate(instance):
                continue

            if as_smac:
                instance = instance.as_smac_instance()  # type: ignore

            verification_instances.append(instance)

    return verification_instances


def read_all_vnncomp_instances(
    vnncomp_path: Path,
) -> dict[str, list[VerificationInstance]]:
    """_summary_."""
    instances: dict[str, list[VerificationInstance]] = {}

    for path in vnncomp_path.iterdir():
        if not path.is_dir():
            continue

        instances[path.name] = read_vnncomp_instances(path.name, vnncomp_path)

    return instances
