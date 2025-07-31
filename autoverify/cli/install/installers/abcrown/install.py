"""abcrown installer."""

from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

AbCrownRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="877afa32d9d314fcb416436a616e6a5878fdab78",
    clone_url="https://github.com/Verified-Intelligence/alpha-beta-CROWN",
)


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs abcrown.

    Args:
        install_dir: Path where ab-crown is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    clone_checkout_verifier(
        AbCrownRepoInfo, 
        install_dir, 
        custom_commit=custom_commit, 
        use_latest=use_latest
    )
    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "environment.yml")
