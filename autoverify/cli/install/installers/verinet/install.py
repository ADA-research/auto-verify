"""verinet installer."""
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

VerinetRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="813e625",
    clone_url="https://github.com/kw-corne/VeriNet",
)


def install(install_dir: Path):
    """_summary_."""
    clone_checkout_verifier(VerinetRepoInfo, install_dir)
    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "environment.yml")
