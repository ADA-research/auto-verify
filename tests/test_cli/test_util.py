import subprocess
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier

DUMMY_CLONE_URL = "https://github.com/example/repo.git"
DUMMY_BRANCH = "main"
DUMMY_COMMIT_HASH = "abcdef123456"


@pytest.fixture
def dummy_repo_info() -> GitRepoInfo:
    return GitRepoInfo(
        branch=DUMMY_BRANCH,
        commit_hash=DUMMY_COMMIT_HASH,
        clone_url=DUMMY_CLONE_URL,
    )


class MockCompletedProcess:
    def __init__(
        self,
        returncode: int,
        stdout: str | None = None,
        stderr: str | None = None,
    ):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


@pytest.fixture
def mock_subprocess_run(monkeypatch: MonkeyPatch):
    def mock_run(*args, **kwargs):
        return MockCompletedProcess(returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_run)


@pytest.fixture
def mock_install_dir(tmp_path: Path) -> Path:
    d = tmp_path / "install_dir"
    (d / "repo").mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture
def dummy_git_repo_info() -> GitRepoInfo:
    return GitRepoInfo(
        branch=DUMMY_BRANCH,
        commit_hash=DUMMY_COMMIT_HASH,
        clone_url=DUMMY_CLONE_URL,
    )


def test_repo_name(dummy_repo_info: GitRepoInfo):
    assert dummy_repo_info.repo_name == "repo"


def test_clone_command(dummy_repo_info: GitRepoInfo):
    expected_cmd = [
        "git",
        "clone",
        DUMMY_CLONE_URL,
        "--depth=1",
        "--branch",
        DUMMY_BRANCH,
    ]
    assert dummy_repo_info.clone == expected_cmd


def test_checkout_command(dummy_repo_info: GitRepoInfo):
    expected_cmd = ["git", "checkout", DUMMY_COMMIT_HASH]
    assert dummy_repo_info.checkout == expected_cmd


def test_clone_checkout_verifier(
    mock_subprocess_run: None,
    dummy_git_repo_info: GitRepoInfo,
    mock_install_dir: Path,
):
    clone_checkout_verifier(dummy_git_repo_info, mock_install_dir)
    assert (mock_install_dir / "tool").is_dir()


def test_clone_checkout_verifier_with_submodules(
    mock_subprocess_run: None,
    dummy_git_repo_info: GitRepoInfo,
    mock_install_dir: Path,
):
    # TODO:
    clone_checkout_verifier(
        dummy_git_repo_info, mock_install_dir, init_submodules=True
    )
