"""Verinet installer."""

from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

VerinetRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="813e625",
    clone_url="https://github.com/kw-corne/VeriNet",
)


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs verinet.

    Args:
        install_dir: Path where verinet is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository with version management
    clone_checkout_verifier(VerinetRepoInfo, install_dir, custom_commit=custom_commit, use_latest=use_latest)

    # Copy environment file and create conda environment
    copy_env_file_to(Path(__file__), install_dir)
    print("Creating conda environment...")
    create_env_from_file(install_dir / "environment.yml")

    # Print installation information
    print("\nVERINET (conda) Installation Complete")
    print(f"Installation directory: {install_dir}")
    print("To activate: conda activate __av__verinet")
