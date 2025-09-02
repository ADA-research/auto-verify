"""Git and git repo utilities."""

import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path

from autoverify.util.env import cwd
from autoverify.util.loggers import install_logger


@dataclass
class GitRepoInfo:
    """Template for a tool's git repo info.

    Attributes:
        branch: The target branch.
        commit_hash: The target commit hash.
        clone_url: The URL the repo will be cloned from.
    """

    branch: str
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
        clone_cmd = f"""git clone --recursive {self.clone_url}\
        --branch {self.branch}"""

        return shlex.split(clone_cmd)

    @property
    def checkout(self) -> list[str]:
        checkout_cmd = f"git checkout {self.commit_hash}"

        return shlex.split(checkout_cmd)


def clone_checkout_verifier(
    repo_info: GitRepoInfo,
    install_dir: Path,
    *,
    init_submodules=False,
    custom_commit=None,
    use_latest=False,
):
    """Clones a verifier and checks out the branch.

    Arguments:
        repo_info: A `GitRepoInfo` object.
        install_dir: Where the repo will be cloned to.
        init_submodules: If submodules in the repository should be initialized.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    with cwd(install_dir):
        install_logger.info(f"Cloning into repository: {repo_info.clone_url}")
        
        # For repositories with problematic submodules, clone without --recursive first
        if init_submodules:
            # Clone without submodules first to avoid SSH issues
            clone_cmd = ["git", "clone", repo_info.clone_url, "--branch", repo_info.branch]
            subprocess.run(clone_cmd, check=True, capture_output=True)
        else:
            subprocess.run(repo_info.clone, check=True, capture_output=True)

        os.rename(install_dir / repo_info.repo_name, install_dir / "tool")

    with cwd(install_dir / "tool"):
        if use_latest:
            install_logger.info(f"Using latest commit on branch {repo_info.branch}")
            # Fetch the latest changes from the remote branch
            try:
                subprocess.run(
                    shlex.split(f"git fetch origin {repo_info.branch}"),
                    check=True,
                    capture_output=True,
                )
                
                # Reset to the latest commit on the branch
                subprocess.run(
                    shlex.split(f"git reset --hard origin/{repo_info.branch}"),
                    check=True,
                    capture_output=True,
                )
                
                # Get the current commit hash for information
                result = subprocess.run(
                    shlex.split("git rev-parse HEAD"),
                    check=True,
                    capture_output=True,
                    text=True,
                )
                commit_hash = result.stdout.strip()
                install_logger.info(f"Latest commit hash: {commit_hash}")
            except subprocess.CalledProcessError:
                install_logger.warning(f"Failed to fetch latest from {repo_info.branch}, using current HEAD")
                # Fall back to current HEAD if fetch fails
                result = subprocess.run(
                    shlex.split("git rev-parse HEAD"),
                    check=True,
                    capture_output=True,
                    text=True,
                )
                commit_hash = result.stdout.strip()
                install_logger.info(f"Current commit hash: {commit_hash}")
        elif custom_commit:
            try:
                # Validate the commit hash format first
                if not validate_commit_hash_format(custom_commit):
                    install_logger.warning(f"Invalid commit hash format: {custom_commit}")
                    raise ValueError(f"Invalid commit hash format: {custom_commit}")
                
                # Validate the commit hash exists
                install_logger.info(f"Validating custom commit hash: {custom_commit}")
                
                # Try to fetch all refs first to ensure we have access to the commit
                subprocess.run(
                    shlex.split("git fetch --all"),
                    check=True,
                    capture_output=True,
                )
                
                # Check if the commit exists
                result = subprocess.run(
                    shlex.split(f"git cat-file -e {custom_commit}"),
                    check=True,
                    capture_output=True,
                )
                
                # If we get here, the commit exists
                install_logger.info(f"Checking out custom commit hash: {custom_commit}")
                checkout_cmd = f"git checkout {custom_commit}"
                subprocess.run(shlex.split(checkout_cmd), check=True, capture_output=True)
            except (subprocess.CalledProcessError, ValueError) as e:
                install_logger.warning(f"Custom commit hash {custom_commit} not found or invalid: {e}")
                install_logger.info(f"Falling back to default commit hash: {repo_info.commit_hash}")
                subprocess.run(repo_info.checkout, check=True, capture_output=True)
        else:
            install_logger.info(f"Checking out default commit hash: {repo_info.commit_hash}")
            subprocess.run(repo_info.checkout, check=True, capture_output=True)

        if init_submodules:
            install_logger.info("Initializing submodules")

            subprocess.run(
                shlex.split("git submodule init"),
                check=True,
                capture_output=True,
            )

            # Handle submodules that might use SSH URLs gracefully
            try:
                subprocess.run(
                    shlex.split("git submodule update"),
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                install_logger.warning(
                    "Failed to update submodules (possibly due to SSH authentication). "
                    "Continuing with partial installation..."
                )
                # Try to update only HTTPS submodules
                try:
                    subprocess.run(
                        shlex.split("git submodule update --init --recursive --remote"),
                        check=False,  # Don't fail on SSH submodules
                        capture_output=True,
                    )
                except Exception:
                    install_logger.warning("Could not update any submodules")


def get_latest_commit_hash(repo_path: Path, branch: str = "main") -> str:
    """Get the latest commit hash for a branch.
    
    Args:
        repo_path: Path to the git repository
        branch: Branch name to check (default: main)
        
    Returns:
        The latest commit hash on the branch
    """
    with cwd(repo_path):
        # Make sure we have the latest from remote
        subprocess.run(
            shlex.split(f"git fetch origin {branch}"),
            check=True,
            capture_output=True,
        )
        
        # Get the latest commit hash
        result = subprocess.run(
            shlex.split(f"git rev-parse origin/{branch}"),
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()


def validate_commit_hash_format(commit_hash: str) -> bool:
    """Validate if a commit hash has a valid format.
    
    Args:
        commit_hash: The commit hash to validate
        
    Returns:
        True if the format is valid, False otherwise
    """
    # Git commit hashes are typically 40 characters (full) or 7+ characters (short)
    if len(commit_hash) < 7 or len(commit_hash) > 40:
        return False
    
    # Git commit hashes are hexadecimal
    try:
        int(commit_hash, 16)
        return True
    except ValueError:
        return False


def validate_commit_hash(repo_path: Path, commit_hash: str) -> bool:
    """Validate if a commit hash exists in the repository.
    
    Args:
        repo_path: Path to the git repository
        commit_hash: The commit hash to validate
        
    Returns:
        True if the commit hash exists, False otherwise
    """
    with cwd(repo_path):
        try:
            subprocess.run(
                shlex.split(f"git cat-file -e {commit_hash}"),
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False
