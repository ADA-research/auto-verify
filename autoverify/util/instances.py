"""_summary_."""
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from autoverify import ROOT_DIR


@dataclass
class VerificationInstance:
    """_summary_."""

    network: Path
    property: Path
    timeout: int | None = None

    def as_smac_instance(self) -> str:
        """Return the instance in a `network,property` format."""
        return f"{str(self.network)},{str(self.property)}"


@dataclass
class VerificationDataResult:
    network: str
    property: str
    success: Literal["OK", "ERR"]
    result: Literal["SAT", "UNSAT", "TIMEOUT"] | None
    counter_example: str | tuple[str, str] | None
    error_string: str | None

    def as_csv_row(self) -> list[str]:
        if isinstance(self.counter_example, tuple):
            self.counter_example = "\n".join(self.counter_example)

        return [
            self.network,
            self.property,
            self.success,
            self.result or "",
            self.counter_example or "",
            self.error_string or "",
        ]


def write_verification_data_results_to_csv(
    results: list[VerificationDataResult], csv_path: Path
):
    """Write a list of `VerificationDataResults` to a csv file."""
    with open(str(csv_path), "a") as csv_file:
        writer = csv.writer(csv_file)

        for result in results:
            writer.writerow(result.as_csv_row())


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
