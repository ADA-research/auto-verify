"""Main CLI entry point for auto-verify."""

import argparse
import logging
import os
import sys
from pathlib import Path

from autoverify import __version__
from autoverify.cli.install import (
    AV_HOME,
    VERIFIER_DIR,
    check_commit_hashes,
    try_install_verifiers,
    try_uninstall_verifiers,
)
from autoverify.cli.install.venv_installers import (
    VENV_VERIFIER_DIR,
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
    install_parser.add_argument(
        "--version", type=str, 
        help="Specific version to install (commit hash or 'most-recent')"
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
    
    # Delete command (alias for uninstall)
    delete_parser = subparsers.add_parser("delete", help="Delete verifiers (alias for uninstall)")
    delete_parser.add_argument(
        "verifiers", nargs="+", help="Verifiers to delete"
    )
    delete_parser.add_argument(
        "--env", choices=["conda", "venv", "both"],
        default="both", help="Which installation type to remove"
    )
    
    # List command
    list_parser = subparsers.add_parser("list", help="List installed verifiers")
    list_parser.add_argument(
        "--env", choices=["conda", "venv", "both"],
        default="both", help="Which installation type to list"
    )
    list_parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed information about each verifier"
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
    
    # Config set-install-path
    set_path_parser = config_subparsers.add_parser("set-install-path", help="Set custom installation path")
    set_path_parser.add_argument(
        "path", type=str, help="Custom installation path (use 'default' to reset to default)"
    )
    
    # Config set-gpu
    set_gpu_parser = config_subparsers.add_parser("set-gpu", help="Set GPU preference")
    set_gpu_parser.add_argument(
        "prefer", choices=["true", "false"], help="Whether to prefer GPU-enabled installations"
    )
    
    # Config set-timeout
    set_timeout_parser = config_subparsers.add_parser("set-timeout", help="Set default timeout")
    set_timeout_parser.add_argument(
        "seconds", type=int, help="Default verification timeout in seconds"
    )
    
    # Config set-log-level
    set_log_parser = config_subparsers.add_parser("set-log-level", help="Set logging verbosity")
    set_log_parser.add_argument(
        "level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
        help="Logging verbosity level"
    )
    
    # Config set-verbose-installation
    set_verbose_parser = config_subparsers.add_parser("set-verbose-installation", help="Set installation verbosity")
    set_verbose_parser.add_argument(
        "verbose", choices=["true", "false"], 
        help="Whether to show detailed output during installation"
    )
    
    # Config set-conda-fallback
    set_fallback_parser = config_subparsers.add_parser("set-conda-fallback", help="Set conda fallback option")
    set_fallback_parser.add_argument(
        "allow", choices=["true", "false"], 
        help="Whether to allow falling back to conda if venv+uv is not available"
    )
    
    # Config set-require-uv
    set_uv_parser = config_subparsers.add_parser("set-require-uv", help="Set uv requirement")
    set_uv_parser.add_argument(
        "require", choices=["true", "false"], 
        help="Whether to require uv when using venv strategy"
    )
    
    # Config example
    config_subparsers.add_parser("example", help="Create example configuration file")
    
    # Config reset
    config_subparsers.add_parser("reset", help="Reset configuration to defaults")
    
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
        try_install_verifiers_venv(args.verifiers, venv_installers, version=args.version)
    else:
        print("Installing with conda environments...")
        try_install_verifiers(args.verifiers, version=args.version)


def _handle_uninstall(args):
    """Handle uninstall command."""
    if args.env in ["conda", "both"]:
        print("Uninstalling conda-based verifiers...")
        try_uninstall_verifiers(args.verifiers)
    
    if args.env in ["venv", "both"]:
        print("Uninstalling venv-based verifiers...")
        try_uninstall_verifiers_venv(args.verifiers)


def _handle_list(args):
    """Handle list command."""
    found_verifiers = False
    
    if args.env in ["conda", "both"]:
        if VERIFIER_DIR.exists():
            conda_verifiers = [d.name for d in VERIFIER_DIR.iterdir() if d.is_dir()]
            if conda_verifiers:
                found_verifiers = True
                print("\nConda-based verifiers:")
                for verifier in sorted(conda_verifiers):
                    print(f"  • {verifier}")
                    if args.verbose:
                        tool_dir = VERIFIER_DIR / verifier / "tool"
                        if tool_dir.exists():
                            try:
                                # Get commit hash
                                import subprocess
                                from autoverify.util.env import cwd
                                with cwd(tool_dir):
                                    result = subprocess.run(
                                        ["git", "rev-parse", "--short", "HEAD"],
                                        capture_output=True,
                                        text=True,
                                        check=True
                                    )
                                    commit = result.stdout.strip()
                                    
                                    # Get branch
                                    result = subprocess.run(
                                        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                        capture_output=True,
                                        text=True,
                                        check=True
                                    )
                                    branch = result.stdout.strip()
                                    
                                    print(f"    - Branch: {branch}")
                                    print(f"    - Commit: {commit}")
                                    print(f"    - Path: {tool_dir}")
                            except Exception:
                                print(f"    - Path: {tool_dir}")
    
    if args.env in ["venv", "both"]:
        if VENV_VERIFIER_DIR.exists():
            venv_verifiers = [d.name for d in VENV_VERIFIER_DIR.iterdir() if d.is_dir()]
            if venv_verifiers:
                found_verifiers = True
                print("\nVenv-based verifiers:")
                for verifier in sorted(venv_verifiers):
                    print(f"  • {verifier}")
                    if args.verbose:
                        tool_dir = VENV_VERIFIER_DIR / verifier / "tool"
                        venv_dir = VENV_VERIFIER_DIR / verifier / "venv"
                        activate_script = VENV_VERIFIER_DIR / verifier / "activate.sh"
                        
                        if tool_dir.exists():
                            try:
                                # Get commit hash
                                import subprocess
                                from autoverify.util.env import cwd
                                with cwd(tool_dir):
                                    result = subprocess.run(
                                        ["git", "rev-parse", "--short", "HEAD"],
                                        capture_output=True,
                                        text=True,
                                        check=True
                                    )
                                    commit = result.stdout.strip()
                                    
                                    # Get branch
                                    result = subprocess.run(
                                        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                        capture_output=True,
                                        text=True,
                                        check=True
                                    )
                                    branch = result.stdout.strip()
                                    
                                    print(f"    - Branch: {branch}")
                                    print(f"    - Commit: {commit}")
                            except Exception:
                                pass
                        
                        if venv_dir.exists():
                            print(f"    - Virtual env: {venv_dir}")
                        
                        if activate_script.exists():
                            print(f"    - Activate: source {activate_script}")
    
    if not found_verifiers:
        print("No verifiers installed.")


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
        
    elif args.config_action == "set-install-path":
        config = get_config()
        if args.path.lower() == "default":
            config.custom_install_path = None
            print("Installation path reset to default")
        else:
            path = Path(args.path).resolve()
            config.custom_install_path = path
            print(f"Installation path set to: {path}")
        
        from autoverify.config import _config_manager
        _config_manager.save_config(config)
        
    elif args.config_action == "set-gpu":
        config = get_config()
        prefer_gpu = args.prefer.lower() == "true"
        config.prefer_gpu = prefer_gpu
        print(f"GPU preference set to: {prefer_gpu}")
        
        from autoverify.config import _config_manager
        _config_manager.save_config(config)
        
    elif args.config_action == "set-timeout":
        config = get_config()
        config.default_timeout = args.seconds
        print(f"Default timeout set to: {args.seconds} seconds")
        
        from autoverify.config import _config_manager
        _config_manager.save_config(config)
        
    elif args.config_action == "set-log-level":
        config = get_config()
        config.log_level = args.level
        print(f"Log level set to: {args.level}")
        
        from autoverify.config import _config_manager
        _config_manager.save_config(config)
        
    elif args.config_action == "set-verbose-installation":
        config = get_config()
        verbose = args.verbose.lower() == "true"
        config.verbose_installation = verbose
        print(f"Verbose installation set to: {verbose}")
        
        from autoverify.config import _config_manager
        _config_manager.save_config(config)
        
    elif args.config_action == "set-conda-fallback":
        config = get_config()
        allow = args.allow.lower() == "true"
        config.allow_conda_fallback = allow
        print(f"Conda fallback set to: {allow}")
        
        from autoverify.config import _config_manager
        _config_manager.save_config(config)
        
    elif args.config_action == "set-require-uv":
        config = get_config()
        require = args.require.lower() == "true"
        config.require_uv = require
        print(f"Require uv set to: {require}")
        
        from autoverify.config import _config_manager
        _config_manager.save_config(config)
        
    elif args.config_action == "example":
        create_example_config()
        
    elif args.config_action == "reset":
        from autoverify.config import _config_manager
        _config_manager.reset_config()


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
        elif args.command == "uninstall" or args.command == "delete":
            _handle_uninstall(args)
        elif args.command == "list":
            _handle_list(args)
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
