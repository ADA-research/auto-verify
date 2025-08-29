"""Main CLI entry point for auto-verify."""

import argparse
import logging
import sys
from pathlib import Path

from autoverify import __version__
from autoverify.cli.install import (
    VERIFIER_DIR,
    check_commit_hashes,
    try_install_verifiers,
    try_uninstall_verifiers,
)
from autoverify.cli.install.installers import repo_infos
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
        description="Auto-verify: Neural network verification toolkit",
        epilog="""
Auto-verify is a toolkit for managing neural network verification tools.
It supports both conda and Python virtual environment management strategies.

For detailed help on any command, use: auto-verify <command> --help
For a comprehensive overview, use: auto-verify help
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--version", action="version", version=f"auto-verify {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Help command
    help_parser = subparsers.add_parser("help", help="Show comprehensive help and examples")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install verifiers")
    install_parser.add_argument(
        "verifiers", nargs="+", help="Verifiers to install (abcrown, nnenum, ovalbab, verinet, mnbab)"
    )
    install_parser.add_argument(
        "--env", choices=["conda", "venv", "auto"], 
        default="conda", help="Environment management strategy (default: conda)"
    )
    install_parser.add_argument(
        "--force-venv", action="store_true",
        help="Force use of venv even if conda is preferred"
    )
    install_parser.add_argument(
        "--verifier-version", type=str, 
        help="Specific verifier version to install (full commit hash or 'most-recent'). "
             "If a short hash is provided, it will fall back to the default version. "
             "Examples: --verifier-version '877afa32d9d314fcb416436a616e6a5878fdab78' or --verifier-version most-recent"
    )
    install_parser.add_argument(
        "--conda-env-name", type=str,
        help="Custom conda environment name (overrides default __av__{verifier} naming)"
    )
    
    # Add helpful epilog
    install_parser.epilog = """
Examples:
  auto-verify install abcrown                    # Install abcrown with default version
  auto-verify install abcrown --verifier-version most-recent  # Install latest version
  auto-verify install abcrown --verifier-version 877afa32d9d314fcb416436a616e6a5878fdab78  # Install specific commit
  auto-verify install abcrown nnenum --env conda  # Install multiple verifiers with conda
  auto-verify install abcrown --env venv          # Force venv installation
  
Note: Use --verifier-version (not --version) to specify verifier versions.
      Use auto-verify --version to see the auto-verify version.
"""
    
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
    check_parser = subparsers.add_parser("check", help="Check verifier status and health")
    check_parser.add_argument(
        "--env", choices=["conda", "venv", "both"],
        default="both", help="Which installation type to check"
    )
    check_parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed status information"
    )
    
    # Versions command
    versions_parser = subparsers.add_parser("versions", help="Show available versions for verifiers")
    versions_parser.add_argument(
        "verifier", help="Name of the verifier to check versions for"
    )
    versions_parser.add_argument(
        "--branch", type=str, default=None,
        help="Branch to check (default: main/master)"
    )
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration settings")
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
    # Check for common user errors
    if hasattr(args, 'version') and args.version:
        print("Error: The --version flag is used to show auto-verify version information.")
        print("To specify a verifier version, use --verifier-version instead.")
        print("Examples:")
        print("  auto-verify --version                    # Show auto-verify version")
        print("  auto-verify install abcrown --verifier-version most-recent")
        print("  auto-verify install abcrown --verifier-version '877afa32d9d314fcb416436a616e6a5878fdab78'")
        return
    
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
        # Default to conda if no preference specified
        use_venv = should_use_venv()
    
    current_strategy = get_env_strategy()
    print(f"Current environment strategy: {current_strategy}")
    print(f"Using {'venv' if use_venv else 'conda'} for installation")
    
    if use_venv:
        print("Installing with Python virtual environments + uv/pip...")
        try_install_verifiers_venv(args.verifiers, venv_installers, version=args.verifier_version)
    else:
        print("Installing with conda environments (recommended)...")
        if args.conda_env_name:
            print(f"Using custom conda environment name: {args.conda_env_name}")
        if args.verifier_version:
            if args.verifier_version == "most-recent":
                print("Installing latest versions of verifiers from their respective branches")
            else:
                print(f"Installing verifiers at specific commit: {args.verifier_version}")
        try_install_verifiers(args.verifiers, version=args.verifier_version)


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
    
    if args.env in ["conda", "both"] and VERIFIER_DIR.exists():
        conda_verifiers = [d.name for d in VERIFIER_DIR.iterdir() if d.is_dir()]
        if conda_verifiers:
            found_verifiers = True
            print("\nConda-based verifiers:")
            for verifier in sorted(conda_verifiers):
                tool_dir = VERIFIER_DIR / verifier / "tool"
                conda_env_name = f"__av__{verifier}"
                
                print(f"  • {verifier}")
                print(f"    - Path: {tool_dir.resolve()}")
                print(f"    - Conda env: {conda_env_name}")
                
                if args.verbose:
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
                                print(f"    - Activate: conda activate {conda_env_name}")
                        except Exception:
                            print(f"    - Activate: conda activate {conda_env_name}")
                    else:
                        print(f"    - Activate: conda activate {conda_env_name}")
                else:
                    print(f"    - Activate: conda activate {conda_env_name}")
    
    if args.env in ["venv", "both"] and VENV_VERIFIER_DIR.exists():
        venv_verifiers = [d.name for d in VENV_VERIFIER_DIR.iterdir() if d.is_dir()]
        if venv_verifiers:
            found_verifiers = True
            print("\nVenv-based verifiers:")
            for verifier in sorted(venv_verifiers):
                tool_dir = VENV_VERIFIER_DIR / verifier / "tool"
                venv_dir = VENV_VERIFIER_DIR / verifier / "venv"
                activate_script = VENV_VERIFIER_DIR / verifier / "activate.sh"
                
                print(f"  • {verifier}")
                print(f"    - Path: {tool_dir.resolve()}")
                
                if args.verbose:
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
                    else:
                        print(f"    - Activate: source {venv_dir}/bin/activate")
                else:
                    if venv_dir.exists():
                        print(f"    - Activate: source {venv_dir}/bin/activate")
    
    if not found_verifiers:
        print("No verifiers installed.")
    
    # Add helpful information about conda
    if args.env in ["conda", "both"]:
        print("\nConda Environment Management:")
        print("  • To activate a verifier: conda activate __av__{verifier_name}")
        print("  • To list all conda envs: conda env list")
        print("  • To remove a conda env: conda env remove -n __av__{verifier_name}")


def _handle_versions(args):
    """Handle versions command."""
    verifier = args.verifier
    
    if verifier not in repo_infos:
        print(f"Error: Unknown verifier '{verifier}'")
        print(f"Available verifiers: {', '.join(repo_infos.keys())}")
        return
    
    repo_info = repo_infos[verifier]
    branch = args.branch or repo_info.branch
    
    print(f"Version information for {verifier}:")
    print(f"  Repository: {repo_info.clone_url}")
    print(f"  Default branch: {repo_info.branch}")
    print(f"  Default commit: {repo_info.commit_hash}")
    print(f"  Checking branch: {branch}")
    
    try:
        from autoverify.cli.util.git import get_latest_commit_hash
        
        # Create a temporary directory to clone and check
        import tempfile
        import shutil
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Clone the repository
            from autoverify.cli.util.git import clone_checkout_verifier
            clone_checkout_verifier(repo_info, temp_path, use_latest=False)
            
            # Get latest commit on the specified branch
            latest_commit = get_latest_commit_hash(temp_path / "tool", branch)
            print(f"  Latest commit on {branch}: {latest_commit}")
            
            if latest_commit != repo_info.commit_hash:
                print(f"  Note: Default commit is {len(repo_info.commit_hash)} characters, latest is {len(latest_commit)} characters")
                print(f"  Consider using: --verifier-version most-recent")
            else:
                print(f"  Default commit is up to date")
                
    except Exception as e:
        print(f"  Error checking latest version: {e}")
        print(f"  You can still install with: --verifier-version most-recent")


def _handle_check(args):
    """Handle check command."""
    print("Checking verifier status...")
    
    if args.env in ["conda", "both"]:
        print("\nChecking conda-based verifiers...")
        check_commit_hashes()
    
    if args.env in ["venv", "both"]:
        print("\nChecking venv-based verifiers...")
        # Check venv verifiers
        if VENV_VERIFIER_DIR.exists():
            venv_verifiers = [d.name for d in VENV_VERIFIER_DIR.iterdir() if d.is_dir()]
            if venv_verifiers:
                print(f"Found {len(venv_verifiers)} venv verifier(s):")
                for verifier in sorted(venv_verifiers):
                    tool_dir = VENV_VERIFIER_DIR / verifier / "tool"
                    venv_dir = VENV_VERIFIER_DIR / verifier / "venv"
                    
                    print(f"  • {verifier}")
                    print(f"    - Path: {tool_dir.resolve()}")
                    
                    if args.verbose:
                        if tool_dir.exists():
                            try:
                                import subprocess
                                from autoverify.util.env import cwd
                                
                                with cwd(tool_dir):
                                    # Get commit hash
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
                            except Exception as e:
                                print(f"    - Error getting git info: {e}")
                        
                        if venv_dir.exists():
                            print(f"    - Virtual env: {venv_dir}")
                            print(f"    - Activate: source {venv_dir}/bin/activate")
                    else:
                        if venv_dir.exists():
                            print(f"    - Activate: source {venv_dir}/bin/activate")
            else:
                print("No venv verifiers found.")
        else:
            print("Venv installation directory not found.")
    
    if args.env not in ["conda", "venv", "both"]:
        print("Invalid environment option. Use: conda, venv, or both")
    
    print("\nVerifier status check complete.")


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
        
        # Show conda-specific information
        if not would_use_venv:
            print("\nConda Environment Information:")
            print("  • Conda is the recommended package manager for auto-verify")
            print("  • Verifiers are installed in isolated conda environments")
            print("  • Environment naming: __av__{verifier_name}")
            print("  • To activate: conda activate __av__{verifier_name}")
        
    elif args.config_action == "set-env":
        set_env_strategy(args.strategy)
        if args.strategy == "conda":
            print("Conda is now the primary environment management strategy.")
            print("This is the recommended approach for auto-verify.")
        
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


def _handle_help():
    """Show comprehensive help and examples."""
    help_text = """
AUTO-VERIFY COMPREHENSIVE HELP
==============================

Auto-verify is a comprehensive toolkit for managing neural network verification tools.
It supports both conda and Python virtual environment management strategies.

SUPPORTED VERIFIERS
------------------
• abcrown    - Neural network verification tool
• nnenum     - Neural network enumeration tool  
• ovalbab    - Neural network verification tool
• verinet    - Neural network verification tool
• mnbab      - Neural network verification tool

CORE COMMANDS
-------------

1. INSTALL VERIFIERS
   auto-verify install <verifier> [options]
   
   Examples:
   • auto-verify install abcrown                    # Install with default version
   • auto-verify install abcrown nnenum            # Install multiple verifiers
   • auto-verify install abcrown --env venv        # Force venv installation
   • auto-verify install abcrown --verifier-version most-recent  # Latest version
   • auto-verify install abcrown --verifier-version <commit-hash>  # Specific version
   
   Options:
   --env {conda,venv,auto}     Environment strategy (default: conda)
   --verifier-version <hash>    Specific commit hash or 'most-recent'
   --conda-env-name <name>      Custom conda environment name
   --force-venv                 Force venv even if conda preferred

2. UNINSTALL VERIFIERS
   auto-verify uninstall <verifier> [options]
   auto-verify delete <verifier> [options]         # Alias for uninstall
   
   Examples:
   • auto-verify uninstall abcrown                 # Remove from both envs
   • auto-verify uninstall abcrown --env conda     # Remove only from conda
   • auto-verify delete abcrown nnenum             # Remove multiple verifiers
   
   Options:
   --env {conda,venv,both}     Which installation to remove (default: both)

3. LIST VERIFIERS
   auto-verify list [options]
   
   Examples:
   • auto-verify list                              # List all verifiers with paths
   • auto-verify list --env conda                  # List only conda installations
   • auto-verify list --verbose                    # Detailed information + paths
   
   Options:
   --env {conda,venv,both}     Which installations to list (default: both)
   --verbose, -v               Show detailed information (git info, etc.)
   
   Note: Full paths are always displayed by default.

4. CHECK VERIFIER STATUS
   auto-verify check [options]
   
   Examples:
   • auto-verify check                             # Check all verifiers with paths
   • auto-verify check --env venv                  # Check only venv installations
   • auto-verify check --verbose                   # Detailed status + paths
   • auto-verify check --env conda --verbose       # Detailed conda status + paths
   
   Options:
   --env {conda,venv,both}     Which installations to check (default: both)
   --verbose, -v               Show detailed status information
   
   Note: Full paths are always displayed by default.

5. SHOW VERIFIER VERSIONS
   auto-verify versions <verifier> [options]
   
   Examples:
   • auto-verify versions abcrown                  # Show available versions
   • auto-verify versions abcrown --branch main    # Check specific branch
   
   Options:
   --branch <branch>            Branch to check (default: main/master)

CONFIGURATION MANAGEMENT
-----------------------

auto-verify config <action> [options]

Available actions:

• show                    - Display current configuration
• set-env <strategy>      - Set environment strategy (conda/venv/auto)
• set-install-path <path> - Set custom installation path
• set-gpu <true/false>    - Set GPU preference
• set-timeout <seconds>   - Set default verification timeout
• set-log-level <level>   - Set logging verbosity (DEBUG/INFO/WARNING/ERROR)
• set-verbose-installation <true/false> - Set installation verbosity
• set-conda-fallback <true/false> - Allow conda fallback
• set-require-uv <true/false> - Require uv for venv strategy
• example                 - Create example configuration file
• reset                   - Reset to default configuration

Examples:
• auto-verify config show                           # Show current config
• auto-verify config set-env conda                 # Prefer conda
• auto-verify config set-log-level DEBUG           # Enable debug logging
• auto-verify config set-timeout 300               # Set 5-minute timeout
• auto-verify config example                       # Create example config

ENVIRONMENT STRATEGIES
---------------------

• conda (default): Use conda environments for package management
• venv: Use Python virtual environments with pip
• auto: Automatically choose based on availability

INSTALLATION PATHS
------------------

• Default conda path: ~/.conda/envs/__av__{verifier}
• Default venv path: ~/.local/share/auto-verify/venv/{verifier}
• Custom paths can be set via config
• Full verifier paths are always displayed in list/check commands

VERSION MANAGEMENT
-----------------

• Default versions: Pre-configured stable commits for each verifier
• Latest versions: Use --verifier-version most-recent
• Specific versions: Use --verifier-version <full-commit-hash>
• Short hashes: Will fall back to default version

TROUBLESHOOTING
---------------

• Use --verbose flags for detailed output
• Check verifier status with: auto-verify check
• Verify installation with: auto-verify list --verbose
• Reset configuration with: auto-verify config reset

GETTING HELP
------------

• auto-verify --help                    # Basic help
• auto-verify help                     # This comprehensive help
• auto-verify <command> --help         # Command-specific help
• auto-verify --version                 # Show version information

For more information, visit the project documentation or repository.
"""
    print(help_text)


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
        elif args.command == "versions":
            _handle_versions(args)
        elif args.command == "config":
            _handle_config(args)
        elif args.command == "help":
            _handle_help()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
