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
from autoverify.verify.eval_verifier import eval_verifier


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--verifier",
        type=str,
        help="Verifier name",
        required=True,
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
        "--warmup",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--output_file",
        type=Path,
        help="CSV file where evaluation data will be saved.",
        required=True,
    )

    config_group = parser.add_mutually_exclusive_group()
    # TODO: Help message
    config_group.add_argument(
        "--config_file",
        type=Path,
        help="File where the configuration is saved, as... TODO",
        default=None,
    )
    # TODO: Help message
    config_group.add_argument(
        "--config_str",
        type=str,
        help="Literal dict... TODO",
        default=None,
    )

    return parser


if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()
    verifier = verifier_from_name(args.verifier.lower())()
    config: Configuration | None = None

    if args.config_str:
        config = parse_config_str_type(args.config_str, verifier.config_space)
    elif args.config_file:
        config = config_from_file(args.config_file, verifier.config_space)

    filter = None
    if args.filter:
        filter = filters[args.filter]

    instances = read_vnncomp_instances(
        args.benchmark,
        args.vnncomp_path,
        predicate=filter,
    )

    assert isinstance(verifier, CompleteVerifier)

    eval_verifier(
        verifier,
        instances,
        config,
        warmup=args.warmup,
        output_csv_path=args.output_file,
    )
