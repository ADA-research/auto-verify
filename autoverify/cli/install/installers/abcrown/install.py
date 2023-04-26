"""abcrown installer."""
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

AbCrownRepoInfo = GitRepoInfo(
    MAIN_BRANCH="main",
    COMMIT_HASH="7b3d507",
    CLONE_URL="https://github.com/Verified-Intelligence/alpha-beta-CROWN",
)


def install(install_dir: Path):
    """_summary_."""
    clone_checkout_verifier(AbCrownRepoInfo, install_dir)
    copy_env_file_to(Path(__file__), install_dir)

    try:
        create_env_from_file(install_dir / "environment.yml")
    except Exception as err:
        print("abcrown install err:")
        print(err)
