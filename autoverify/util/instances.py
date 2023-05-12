"""_summary_."""
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

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


def read_vnncomp_instances(benchmark: str) -> list[VerificationInstance]:
    """_summary_."""
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
                    int(timeout),
                )
            )

    return verification_instances
