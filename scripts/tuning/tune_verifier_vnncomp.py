"""CLI interface for tuning a verifier on a VNNCOMP-like benchmark."""
import argparse
from pathlib import Path

from autoverify.tune import smac_tune_verifier
from autoverify.tune.tune_verifier import vnn_smac_tune_verifier
from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp_filters import filters


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--verifier",
        type=str,
        help="Verifier name",
        required=True,
    )
    parser.add_argument(
        "--benchmark",
        type=str,
        help="Name of the VNNCOMP benchmark",
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
        type=Path,
        help="Path to VNNCOMP benchmarks",
        required=True,
    )
    parser.add_argument(
        "--filter",
        type=str,
        help="Name of filter for instances",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        help="SMAC output directory",
    )
    parser.add_argument(
        "--run_name",
        type=str,
        help="Name of the SMAC run.",
    )
    parser.add_argument(
        "--rh_csv_path",
        type=Path,
        help="Path where the RunHistory will be written to.",
    )
    parser.add_argument(
        "--config_out",
        type=str,
        help="Config output file",
    )

    return parser


if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()
    print(args)

    verifier = verifier_from_name(args.verifier.lower())()
    vnncomp_path = Path(args.vnncomp_path)
    output_dir = Path(args.output_dir) if args.output_dir else None
    config_out = Path(args.config_out) if args.config_out else None

    if not vnncomp_path.is_dir():
        raise ValueError(f"{vnncomp_path} is not a valid directory")

    if output_dir and not output_dir.is_dir():
        output_dir.mkdir(parents=True, exist_ok=True)

    filter = None
    if args.filter:
        filter = filters[args.filter]

    instances = read_vnncomp_instances(
        args.benchmark,
        vnncomp_path,
        as_smac=True,
        predicate=filter,
    )

    config = vnn_smac_tune_verifier(
        args.verifier.lower(),
        instances,
        args.benchmark,
        args.time,
        output_dir=output_dir,
        config_out=config_out,
        run_name=args.run_name,
        rh_csv_path=args.rh_csv_path,
    )

    # config = smac_tune_verifier(
    #     verifier,
    #     instances,
    #     args.time,
    #     output_dir=output_dir,
    #     config_out=config_out,
    #     run_name=args.run_name,
    #     rh_csv_path=args.rh_csv_path,
    # )

    print("*" * 80)
    print("Incumbent:")
    print(config)
    print("*" * 80)
