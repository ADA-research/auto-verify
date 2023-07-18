import argparse
from pathlib import Path

from autoverify.tune import smac_tune_verifier
from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp_filters import filters

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--verifier",
        type=str,
        help="Verifier name",
        required=True,
    )
    parser.add_argument(
        "--time",
        type=int,
        help="Walltime limit",
        required=True,
    )
    parser.add_argument(
        "--vnncomp_path",
        type=str,
        help="Path to VNNCOMP benchmarks",
        required=True,
    )
    parser.add_argument(
        "--benchmark",
        type=str,
        help="Name of the VNNCOMP benchmark",
        required=True,
    )
    parser.add_argument(
        "--filter",
        type=str,
        help="Name of filter for instances",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="SMAC output directory",
    )
    parser.add_argument(
        "--config_out",
        type=str,
        help="Config output file",
    )
    args = parser.parse_args()

    verifier = verifier_from_name(args.verifier.lower())()
    vnncomp_path = Path(args.vnncomp_path)
    output_dir = Path(args.output_dir) if args.output_dir else None
    config_out = Path(args.config_out) if args.config_out else None

    if not vnncomp_path.is_dir():
        raise ValueError(f"{vnncomp_path} is not a valid directory")

    filter = None
    if args.filter:
        filter = filters[args.filter]

    instances = read_vnncomp_instances(
        args.benchmark,
        vnncomp_path,
        as_smac=True,
        predicate=filter,
    )

    config = smac_tune_verifier(
        verifier,
        instances,
        args.time,
        output_dir=output_dir,
        config_out=config_out,
    )

    print("*" * 80)
    print("Incumbent:")
    print(config)
    print("*" * 80)
