"""Git and repo utilities."""
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path

from autoverify.util.loggers import install_logger


@dataclass
class GitRepoInfo:
    """Template for a tool's git repo info."""

    main_branch: str
    commit_hash: str
    clone_url: str

    @property
    def repo_name(self) -> str:
        return (
            self.clone_url.rstrip("/")
            .rsplit("/", maxsplit=1)[-1]
            .removesuffix(".git")
        )

    @property
    def clone(self) -> list[str]:
        clone_cmd = (
            f"git clone {self.clone_url} --depth=1 "
            f"--branch {self.main_branch}"
        )

        return shlex.split(clone_cmd)

    @property
    def checkout(self) -> list[str]:
        checkout_cmd = f"git checkout {self.commit_hash}"

        return shlex.split(checkout_cmd)


def clone_checkout_verifier(repo_info: GitRepoInfo, install_dir: Path):
    """_summary_."""
    os.chdir(install_dir)

    install_logger.info(f"Cloning into repository: {repo_info.clone_url}")
    subprocess.run(repo_info.clone, check=True, capture_output=True)

    os.rename(install_dir / repo_info.repo_name, install_dir / "tool")
    os.chdir(install_dir / "tool")

    install_logger.info(f"Checking out commit hash {repo_info.commit_hash}")
    subprocess.run(repo_info.checkout, check=True, capture_output=True)
