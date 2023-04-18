"""nnenum installer."""
import os
import subprocess
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

NnenumRepoInfo = GitRepoInfo(
    MAIN_BRANCH="master",
    COMMIT_HASH="cf7c0e7",
    CLONE_URL="https://github.com/stanleybak/nnenum.git",
)


# TODO: clone + checkout to a util function or something, other installers will
# do the same thing.
def install(install_dir: Path):
    """_summary_."""
    os.chdir(install_dir)

    subprocess.run(NnenumRepoInfo.clone, check=True, capture_output=True)

    os.rename(install_dir / NnenumRepoInfo.repo_name, install_dir / "tool")
    os.chdir(install_dir / "tool")

    subprocess.run(NnenumRepoInfo.checkout, check=True, capture_output=True)

    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "conda_env.yml")
