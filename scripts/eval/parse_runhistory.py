import argparse
from pathlib import Path

from autoverify.util.smac import get_smac_run_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "smac_run_path", type=Path, help="Path to the SMAC run, seed specific"
    )

    args = parser.parse_args()
    run_data = get_smac_run_data(args.smac_run_path)

    print(f"SMAC data for {args.smac_run_path.parent.name}:")
    for k, v in run_data.items():
        print(k, v)
