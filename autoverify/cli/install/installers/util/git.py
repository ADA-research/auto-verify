"""Git and repo utilities."""
import shlex
from dataclasses import dataclass


@dataclass
class GitRepoInfo:
    """Template for a tool's git repo info."""

    MAIN_BRANCH: str
    COMMIT_HASH: str
    CLONE_URL: str

    @property
    def repo_name(self) -> str:
        return (
            self.CLONE_URL.rstrip("/")
            .rsplit("/", maxsplit=1)[-1]
            .removesuffix(".git")
        )

    @property
    def clone(self) -> list[str]:
        clone_cmd = (
            f"git clone {self.CLONE_URL} --depth=1 "
            f"--branch {self.MAIN_BRANCH}"
        )

        return shlex.split(clone_cmd)

    @property
    def checkout(self) -> list[str]:
        checkout_cmd = f"git checkout {self.COMMIT_HASH}"

        return shlex.split(checkout_cmd)
