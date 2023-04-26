"""nnenum installer."""
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

NnenumRepoInfo = GitRepoInfo(
    MAIN_BRANCH="master",
    COMMIT_HASH="cf7c0e7",
    CLONE_URL="https://github.com/stanleybak/nnenum.git",
)


def install(install_dir: Path):
    """_summary_."""
    clone_checkout_verifier(NnenumRepoInfo, install_dir)
    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "environment.yml")
