"""nnenum installer."""
import os
import subprocess
from pathlib import Path

from .util.env import create_env_file
from .util.git import GitRepoInfo

NnenumRepoInfo = GitRepoInfo(
    MAIN_BRANCH="master",
    COMMIT_HASH="cf7c0e7",
    CLONE_URL="https://github.com/stanleybak/nnenum.git",
)


# TODO: clone + checkout to a util function, other installers will probably
# do the same thing.
def install(install_dir: Path):
    """_summary_."""
    os.chdir(install_dir)

    subprocess.run(NnenumRepoInfo.clone, check=True, capture_output=True)

    os.rename(install_dir / NnenumRepoInfo.repo_name, install_dir / "tool")
    os.chdir(install_dir / "tool")

    subprocess.run(NnenumRepoInfo.checkout, check=True, capture_output=True)

    create_env_file(install_dir)
