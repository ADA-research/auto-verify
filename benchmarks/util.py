"""_summary_."""
import csv
from pathlib import Path
from typing import Any

from autoverify.util.env import get_file_path


def read_vnncomp_instances(
    benchmark: str,
    *,
    as_smac_instances=False,
) -> list[Any]:  # TODO: No any
    """_summary_."""
    vnncomp2022 = get_file_path(Path(__file__)) / "vnncomp2022"
    benchmark_dir = vnncomp2022 / benchmark
    instances = benchmark_dir / "instances.csv"

    verification_instances = []

    with open(str(instances)) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            network, property, timeout = row
            abs_network = str(benchmark_dir / network)
            abs_property = str(benchmark_dir / property)

            instance_row: list[str | int] | str

            if not as_smac_instances:
                instance_row = [abs_network, abs_property, int(timeout)]
            else:
                instance_row = f"{abs_network},{abs_property}"

            verification_instances.append(instance_row)

    return verification_instances
