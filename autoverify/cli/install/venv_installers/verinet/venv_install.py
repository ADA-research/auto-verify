"""verinet venv installer."""

from pathlib import Path

from autoverify.cli.install.venv_installers.venv_install import (
    create_verifier_venv,
    install_requirements,
)
from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from result import Ok

VenvVerinetRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="813e625",
    clone_url="https://github.com/kw-corne/VeriNet",
)


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs verinet with venv.

    Args:
        install_dir: Path where verinet is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository
    clone_checkout_verifier(
        VenvVerinetRepoInfo, 
        install_dir, 
        custom_commit=custom_commit, 
        use_latest=use_latest
    )
    
    # Create virtual environment
    venv_result = create_verifier_venv(install_dir, "verinet")
    venv_path = venv_result.unwrap()
    
    # Define requirements
    requirements = [
        "numpy>=1.21.0",
        "torch>=1.11.0",
        "onnx>=1.12.0",
        "onnxruntime>=1.12.0",
        "scipy>=1.7.0",
    ]
    
    # Install requirements
    install_requirements(venv_path, requirements)
    
    # Print installation information
    print("\nVERINET (venv) Installation Complete")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")
    
    return Ok() 