"""_summary_."""
import csv
from pathlib import Path

from autoverify.util.env import get_file_path


def read_vnncomp_instances(benchmark: str) -> list[str]:
    """_summary_."""
    vnncomp2022 = get_file_path(Path(__file__)) / "vnncomp2022"
    benchmark_dir = vnncomp2022 / benchmark
    instances = benchmark_dir / "instances.csv"

    verification_instances = []

    with open(str(instances)) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            network, property, timeout = row
            verification_instances.append(
                [
                    str(benchmark_dir / network),
                    str(benchmark_dir / property),
                    timeout,  # TODO: Is the 3rd field even the timeout
                ]
            )

    return verification_instances
