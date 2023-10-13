import subprocess
from pathlib import Path


def run_av_cli(args: list[str]) -> str:
    base_cmd = ["auto-verify"]
    base_cmd.extend(args)

    result = subprocess.run(base_cmd, stdout=subprocess.PIPE)
    return str(result.stdout)


def read_csv_contents(csv_path: Path) -> str:
    with open(str(csv_path), "r") as csv_file:
        return csv_file.read()
