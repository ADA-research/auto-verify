"""CLI entry point module."""
import argparse
import sys

from autoverify import __version__ as AV_VERSION
from autoverify.util.verifiers import get_all_complete_verifier_names

from .install import try_install_verifiers, try_uninstall_verifiers


def _build_arg_parser() -> argparse.ArgumentParser:
    """Setup the cli arg options."""
    parser = argparse.ArgumentParser()

    # FIXME: This command and others are slow on bad hardware; Likely because
    # we are importing many elements from the package which takes a while.
    parser.add_argument("-V", "--version", action="version", version=AV_VERSION)

    subparsers = parser.add_subparsers(
        title="subcommands",
        help="""(un)install specified verifiers and exit, run install --help
        for a list of available options""",
    )

    install_parser = subparsers.add_parser("install")
    uninstall_parser = subparsers.add_parser("uninstall")

    install_parser.add_argument(
        "install",
        nargs="+",
        choices=get_all_complete_verifier_names(),
        help="install specified verifiers and exit",
    )

    uninstall_parser.add_argument(
        "uninstall",
        nargs="+",
        choices=get_all_complete_verifier_names(),
        help="uninstall specified verifiers and exit",
    )

    return parser


def main():
    """Parse and process cli args."""
    parser = _build_arg_parser()
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if hasattr(args, "install"):
        try_install_verifiers(args.install)
    elif hasattr(args, "uninstall"):
        try_uninstall_verifiers(args.uninstall)


if __name__ == "__main__":
    main()
