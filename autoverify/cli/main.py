"""Main CLI entry point for auto-verify."""

import argparse
import logging
import sys

from autoverify import __version__
from autoverify.cli.install import (
    check_commit_hashes,
    try_install_verifiers,
    try_uninstall_verifiers,
)
from autoverify.cli.install.venv_installers import (
    try_install_verifiers_venv,
    try_uninstall_verifiers_venv,
    venv_installers,
)
from autoverify.config import (
    create_example_config,
    get_config,
    get_env_strategy,
    set_env_strategy,
    should_use_venv,
)


def _build_arg_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="Auto-verify: Neural network verification toolkit"
    )
    
    parser.add_argument(
        "--version", action="version", version=f"auto-verify {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install verifiers")
    install_parser.add_argument(
        "verifiers", nargs="+", help="Verifiers to install"
    )
    install_parser.add_argument(
        "--env", choices=["conda", "venv", "auto"], 
        help="Environment management strategy (overrides config)"
    )
    install_parser.add_argument(
        "--force-venv", action="store_true",
        help="Force use of venv even if conda is preferred"
    )
    
    # Uninstall command
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall verifiers")
    uninstall_parser.add_argument(
        "verifiers", nargs="+", help="Verifiers to uninstall"
    )
    uninstall_parser.add_argument(
        "--env", choices=["conda", "venv", "both"],
        default="both", help="Which installation type to remove"
    )
    
    # Check command
    subparsers.add_parser("check", help="Check verifier status")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_subparsers = config_parser.add_subparsers(dest="config_action")
    
    # Config show
    config_subparsers.add_parser("show", help="Show current configuration")
    
    # Config set-env
    set_env_parser = config_subparsers.add_parser("set-env", help="Set environment strategy")
    set_env_parser.add_argument(
        "strategy", choices=["conda", "venv", "auto"],
        help="Environment management strategy"
    )
    
    # Config example
    config_subparsers.add_parser("example", help="Create example configuration file")
    
    return parser


def _handle_install(args):
    """Handle install command."""
    # Determine which installation method to use
    use_venv = args.force_venv
    
    if not use_venv and args.env:
        if args.env == "venv":
            use_venv = True
        elif args.env == "conda":
            use_venv = False
        elif args.env == "auto":
            use_venv = should_use_venv()
    elif not use_venv:
        use_venv = should_use_venv()
    
    current_strategy = get_env_strategy()
    print(f"Current environment strategy: {current_strategy}")
    print(f"Using {'venv' if use_venv else 'conda'} for installation")
    
    if use_venv:
        print("Installing with Python virtual environments + uv/pip...")
        try_install_verifiers_venv(args.verifiers, venv_installers)
    else:
        print("Installing with conda environments...")
        try_install_verifiers(args.verifiers)


def _handle_uninstall(args):
    """Handle uninstall command."""
    if args.env in ["conda", "both"]:
        print("Uninstalling conda-based verifiers...")
        try_uninstall_verifiers(args.verifiers)
    
    if args.env in ["venv", "both"]:
        print("Uninstalling venv-based verifiers...")
        try_uninstall_verifiers_venv(args.verifiers)


def _handle_check(args):
    """Handle check command."""
    check_commit_hashes()


def _handle_config(args):
    """Handle config command."""
    if args.config_action == "show":
        config = get_config()
        print("Auto-verify Configuration:")
        print(f"  Environment strategy: {config.env_strategy}")
        print(f"  Custom install path: {config.custom_install_path}")
        print(f"  Prefer GPU: {config.prefer_gpu}")
        print(f"  Default timeout: {config.default_timeout}")
        print(f"  Log level: {config.log_level}")
        print(f"  Verbose installation: {config.verbose_installation}")
        print(f"  Allow conda fallback: {config.allow_conda_fallback}")
        print(f"  Require uv: {config.require_uv}")
        
        # Show what would be used
        would_use_venv = should_use_venv()
        print(f"\nBased on current config and system: would use {'venv' if would_use_venv else 'conda'}")
        
    elif args.config_action == "set-env":
        set_env_strategy(args.strategy)
        
    elif args.config_action == "example":
        create_example_config()


def main():
    """Main entry point."""
    parser = _build_arg_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Set up logging
    logging.basicConfig(
        level=getattr(logging, get_config().log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    try:
        if args.command == "install":
            _handle_install(args)
        elif args.command == "uninstall":
            _handle_uninstall(args)
        elif args.command == "check":
            _handle_check(args)
        elif args.command == "config":
            _handle_config(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
