"""_summary_."""
import csv
import inspect
from dataclasses import dataclass, fields, is_dataclass
from pathlib import Path
from typing import Any, Literal

import pandas as pd

from autoverify import ROOT_DIR


@dataclass
class VerificationInstance:
    """_summary_."""

    network: Path
    property: Path
    timeout: int | None = None

    def as_smac_instance(self) -> str:
        """Return the instance in a `f"{network},{property}"` format.

        A SMAC instance has to be passed as a single string to the
        target_function, in which we split the instance string on the comma
        again to obtain the network and property.
        """
        return f"{str(self.network)},{str(self.property)}"


# TODO: Move this function to another file, it doesn't really belong here
# NOTE: There is no type annotation for dataclasses
def get_dataclass_field_names(data_cls: Any) -> list[str]:
    """Returns the fields of a dataclass as a list of strings."""
    if not inspect.isclass(data_cls):
        raise ValueError(f"Argument data_cls should be a class, got {data_cls}")

    if not is_dataclass(data_cls):
        raise ValueError(f"'{data_cls.__class__.__name__}' is not a dataclass")

    return [field.name for field in fields(data_cls)]


@dataclass
class VerificationDataResult:
    """_summary_."""

    network: str
    property: str
    verifier: str
    config: str
    success: Literal["OK", "ERR"]  # TODO: Why not just a boolean?
    result: Literal["SAT", "UNSAT", "TIMEOUT"] | None
    took: float
    counter_example: str | tuple[str, str] | None
    error_string: str | None

    def as_csv_row(self) -> list[str]:
        """Convert data to a csv row writeable."""
        if isinstance(self.counter_example, tuple):
            self.counter_example = "\n".join(self.counter_example)

        return [
            self.network,
            self.property,
            self.verifier,
            self.config,
            self.success,
            self.result or "",
            str(self.took),
            self.counter_example or "",
            self.error_string or "",
        ]


def init_verification_result_csv(csv_path: Path):
    """_summary_."""
    with open(str(csv_path), "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(get_dataclass_field_names(VerificationDataResult))


def append_verification_result_to_csv(
    verification_result: VerificationDataResult, csv_path: Path
):
    """_summary_."""
    with open(str(csv_path), "a") as csv_file:
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
    instances: list[VerificationInstance],
) -> list[str]:
    """_summary_."""
    return [inst.as_smac_instance() for inst in instances]


def read_vnncomp_instances(benchmark: str) -> list[VerificationInstance]:
    """Read the instances of a VNNCOMP benchmark.

    Reads the CSV file of a VNNCOMP benchmark, parsing the network, property and
    timeout values.

    Args:
        benchmark: The name of the benchmark directory.

    Returns:
        list[VerificationInstance]: A list of `VerificationInstance` objects
            that hold the network, property and timeout.
    """
    vnncomp2022 = ROOT_DIR.parent / "benchmarks" / "vnncomp2022"
    benchmark_dir = vnncomp2022 / benchmark
    instances = benchmark_dir / "instances.csv"

    verification_instances = []

    with open(str(instances)) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            network, property, timeout = row
            abs_network = str(benchmark_dir / network)
            abs_property = str(benchmark_dir / property)

            verification_instances.append(
                VerificationInstance(
                    Path(abs_network),
                    Path(abs_property),
                    int(timeout),  # TODO: Is that always an integer?
                )
            )

    return verification_instances
