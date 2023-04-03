"""CLI entry point module."""
import argparse
import sys

import autoverify


def build_arg_parser() -> argparse.ArgumentParser:
    """Setup the cli arg options."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-V", "--version", action="version", version=autoverify.__version__
    )
    # TODO: set choices to real verifiers
    parser.add_argument(
        "--install",
        choices=["a", "b", "c"],
        help="install specified verifiers and exit",
    )

    return parser


def main():
    """Parse and process cli args."""
    parser = build_arg_parser()

    # print the help message if no args were specified
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    print(args)

    return 1


if __name__ == "__main__":
    main()
