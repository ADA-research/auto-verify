"""_summary_."""
import csv
from dataclasses import dataclass
from pathlib import Path

from autoverify import ROOT_DIR


@dataclass
class VerificationInstance:
    """_summary_."""

    network: Path
    property: Path
    timeout: int | None = None

    def as_smac_instance(self) -> str:
        return f"{str(self.network)},{str(self.property)}"


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
