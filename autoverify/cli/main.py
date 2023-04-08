"""CLI entry point module."""
import argparse
import sys

from result import Err, Ok

from autoverify import __version__ as AV_VERSION
from autoverify.cli.install.install import try_install_verifiers
from autoverify.util.verifiers import get_all_complete_verifier_names

from .install import try_install_verifiers


def build_arg_parser() -> argparse.ArgumentParser:
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
    parser = build_arg_parser()

    # print the help message if no args were specified
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args.install:
        try_install_verifiers(args.install)
        # install_result = install_verifiers(args.install)
        #
        # # TODO: real logging
        # if isinstance(install_result, Ok):
        #     print(f"Success, {install_result.value}")
        # elif isinstance(install_result, Err):
        #     print(f"Failure, {install_result.value}")
        #


if __name__ == "__main__":
    main()
