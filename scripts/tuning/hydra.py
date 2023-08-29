import argparse
from pathlib import Path

from autoverify.tune.tune_hydra import tune_hydra_portfolio
from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.resource_strategy import (
    ResourceStrategy,
    resources_from_strategy,
)
from autoverify.util.vnncomp_filters import filters


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--verifiers",
        nargs="+",
        type=str,
        help="Verifiers to consider",
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
        "--filter",
        type=str,
        help="Name of filter for instances",
    )
    parser.add_argument(
        "--length",
        type=int,
        help="Length of the portfolio",
        required=True,
    )
    parser.add_argument(
        "--sec_per_iter",
        type=int,
        help="Walltime limit per Hydra iteration",
        required=True,
    )
    parser.add_argument(
        "--alpha",
        type=float,
        help="Alpha (in [0, 1]), tune/pick split",
        required=True,
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        help="Hydra output directory",
        required=True,
    )
    parser.add_argument(
        "--portfolio_out",
        type=Path,
        help="Portfolio output file",
        required=True,
    )
    parser.add_argument(
        "--configs_per_iter",
        type=int,
        help="Configurations to tune per Hydra iteration",
        default=1,
    )
    parser.add_argument(
        "--added_per_iter",
        type=int,
        help="Number of configs added to the portfolio per Hydra iteration",
        default=1,
    )
    parser.add_argument(
        "--stop_early",
        type=bool,
        help="Wether to stop early when performance stagnates",
        default=False,
    )
    parser.add_argument(
        "--resource_strategy",
        type=str,
        choices=[v.value for v in ResourceStrategy],
        help="Resource allocation strategy",
        default="auto",
    )
    parser.add_argument(
        "--vnn_compat",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Use VNNCOMP compatible mode",
    )

    return parser


if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()

    instances = read_vnncomp_instances(
        args.benchmark,
        vnncomp_path=args.vnncomp_path,
        predicate=filters.get(args.filter),
    )

    args.resource_strategy = ResourceStrategy(args.resource_strategy)
    resources = resources_from_strategy(args.resource_strategy, args.verifiers)

    tune_hydra_portfolio(
        instances,
        args.verifiers,
        resources,
        args.alpha,
        args.length,
        args.sec_per_iter,
        args.output_dir,
        args.portfolio_out,
        configs_per_iter=args.configs_per_iter,
        added_per_iter=args.added_per_iter,
        stop_early=args.stop_early,
        resource_strategy=args.resource_strategy,
        vnn_compat_mode=args.vnn_compat,
        benchmark=args.benchmark,
    )
