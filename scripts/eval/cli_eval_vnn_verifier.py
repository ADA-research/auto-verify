import argparse
from pathlib import Path

from autoverify.verify.eval_verifier import eval_vnn_verifier


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
        "--vnncomp_path",
        type=Path,
        help="Path to VNNCOMP benchmarks",
        required=True,
    )

    parser.add_argument(
        "--vnn_configs_dir",
        type=Path,
        help="Directory where the VNNCOMP configs are stored.",
        required=True,
    )
    parser.add_argument(
        "--warmup",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Perform a short (10 sec) warmup run.",
    )
    parser.add_argument(
        "--csv_file",
        type=Path,
        help="CSV file where evaluation data will be saved.",
        required=True,
    )

    return parser


if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()

    eval_vnn_verifier(
        args.verifier,
        args.benchmark,
        args.vnncomp_path,
        args.csv_file,
        args.vnn_configs_dir,
        warmup=args.warmup,
    )
