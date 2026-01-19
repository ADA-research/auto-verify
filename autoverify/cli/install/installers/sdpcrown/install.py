"""SDP-CROWN installer."""

from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

SDPCrownRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="84d041375aaff3c2f872570438c564c97fcb7170",
    clone_url="https://github.com/henba1/SDP-CROWN_auto-verify.git",
)


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs SDP-CROWN.

    Args:
        install_dir: Path where SDP-CROWN is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository with version management
    clone_checkout_verifier(SDPCrownRepoInfo, install_dir, custom_commit=custom_commit, use_latest=use_latest)

    # Copy environment file and create conda environment
    copy_env_file_to(Path(__file__), install_dir)
    print("Creating conda environment...")
    create_env_from_file(install_dir / "environment.yml")

    # Print installation information
    print("\nSDP-CROWN (conda) Installation Complete")
    print(f"Installation directory: {install_dir}")
    print("To activate: conda activate __av__sdpcrown")
    print("To use: python -m autoverify.verifier.complete.sdpcrown.sdpcrown_runner")
