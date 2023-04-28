"""nnenum installer."""
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

MnBabRepoInfo = GitRepoInfo(
    MAIN_BRANCH="main",
    COMMIT_HASH="6aa5272",
    CLONE_URL="https://github.com/eth-sri/mn-bab",
)


# TODO: Make the env file, most deps are on anaconda
def install(install_dir: Path):
    """_summary_."""
    clone_checkout_verifier(MnBabRepoInfo, install_dir)
    # copy_env_file_to(Path(__file__), install_dir)
    # create_env_from_file(install_dir / "environment.yml")
