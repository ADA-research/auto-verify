"""abcrown installer."""
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

AbCrownRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="7b3d507",
    clone_url="https://github.com/Verified-Intelligence/alpha-beta-CROWN",
)


def install(install_dir: Path):
    """Installs abcrown.

    Args:
        install_dir: Path where ab-crown is installed.
    """
    clone_checkout_verifier(AbCrownRepoInfo, install_dir)
    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "environment.yml")
