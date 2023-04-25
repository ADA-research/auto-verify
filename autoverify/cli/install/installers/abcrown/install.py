"""abcrown installer."""
import os
import subprocess
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

AbCrownRepoInfo = GitRepoInfo(
    MAIN_BRANCH="main",
    COMMIT_HASH="7b3d507",
    CLONE_URL="https://github.com/Verified-Intelligence/alpha-beta-CROWN",
)


# TODO: clone + checkout to a util function or something, other installers will
# do the same thing.
def install(install_dir: Path):
    """_summary_."""
    os.chdir(install_dir)

    subprocess.run(AbCrownRepoInfo.clone, check=True, capture_output=True)

    os.rename(install_dir / AbCrownRepoInfo.repo_name, install_dir / "tool")
    os.chdir(install_dir / "tool")

    subprocess.run(AbCrownRepoInfo.checkout, check=True, capture_output=True)

    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "conda_env.yml")
