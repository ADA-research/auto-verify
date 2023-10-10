"""nnenum installer."""
from pathlib import Path

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.conda import create_env_from_file
from autoverify.util.env import copy_env_file_to

NnenumRepoInfo = GitRepoInfo(
    branch="vnncomp2022",
    commit_hash="c68562d",
    clone_url="https://github.com/kw-corne/nnenum",
)


def install(install_dir: Path):
    """Installs nnenum.

    Args:
        install_dir: Path where ab-crown is installed.
    """
    clone_checkout_verifier(NnenumRepoInfo, install_dir)
    copy_env_file_to(Path(__file__), install_dir)
    create_env_from_file(install_dir / "environment.yml")
