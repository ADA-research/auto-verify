"""CLI interface for evaluating a verifier on a VNNCOMP-like benchmark."""
import argparse
from pathlib import Path

from ConfigSpace import Configuration

from autoverify.util.cli import parse_config_str_type
from autoverify.util.configs import config_from_file
from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.verifiers import verifier_from_name
from autoverify.util.vnncomp_filters import filters
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verify.eval_verifier import (
    eval_verifier,
    eval_verifier_vnncompat,
)


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--verifier",
        type=str,
        help="Verifier name",
        required=True,
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=True,
        required=False,
        help="Path to the configuration.txt",
    )
    parser.add_argument(
        "--vnncomp_path",
        type=Path,
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
        "--vnn_compat",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Use VNN compatible mode",
    )
    parser.add_argument(
        "--warmup",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Perform a short (10 sec) warmup run.",
    )
    parser.add_argument(
        "--output_file",
        type=Path,
        help="CSV file where evaluation data will be saved.",
        required=True,
    )

    return parser


if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()
    verifier = verifier_from_name(args.verifier)()
    assert isinstance(verifier, CompleteVerifier)

    config_path: Path | None = args.config
    config: Configuration | None = None

    if config_path:
        config = config_from_file(config_path, verifier.config_space)

    filter = None
    if args.filter:
        filter = filters[args.filter]

    instances = read_vnncomp_instances(
        args.benchmark,
        args.vnncomp_path,
        predicate=filter,
    )

    if not args.vnn_compat:
        eval_verifier(
            verifier,
            instances,
            config,
            warmup=args.warmup,
            output_csv_path=args.output_file,
        )
    else:
        eval_verifier_vnncompat(
            args.verifier,
            args.benchmark,
            instances,
            config,
            warmup=args.warmup,
            output_csv_path=args.output_file,
        )