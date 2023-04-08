"""CLI entry point module."""
import argparse
import sys

from autoverify import __version__ as AV_VERSION
from autoverify.util.verifiers import get_all_complete_verifier_names

from .install import try_install_verifiers


def _build_arg_parser() -> argparse.ArgumentParser:
    """Setup the cli arg options."""
    parser = argparse.ArgumentParser()

    parser.add_argument("-V", "--version", action="version", version=AV_VERSION)

    parser.add_argument(
        "--install",
        nargs="+",
        choices=get_all_complete_verifier_names(),
        help="install specified verifiers and exit",
    )

    return parser


def main():
    """Parse and process cli args."""
    parser = _build_arg_parser()
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args.install:
        try_install_verifiers(args.install)


if __name__ == "__main__":
    main()
