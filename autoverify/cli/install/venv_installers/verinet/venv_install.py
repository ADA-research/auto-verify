"""verinet venv-based installer."""

from pathlib import Path

from autoverify.cli.install.venv_installers.venv_install import (
    create_verifier_venv,
    install_requirements,
)
from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier

VenvVerinetRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="e7e82c3",  # Update to latest stable commit
    clone_url="https://github.com/vas-group-imperial/VeriNet",
)


def install(install_dir: Path):
    """
    Installs verinet using virtual environment and uv/pip.

    Args:
        install_dir: Path where verinet is installed.
    """
    # Clone the repository
    clone_checkout_verifier(VenvVerinetRepoInfo, install_dir)
    
    # Create virtual environment
    venv_result = create_verifier_venv(install_dir)
    if venv_result.is_err():
        raise Exception(f"Failed to create venv: {venv_result.unwrap_err()}")
        
    venv_path = venv_result.unwrap()
    
    # Define requirements for verinet
    requirements = [
        "torch>=2.0.0",
        "torchvision",
        "numpy>=1.24.0", 
        "onnx>=1.13.0",
        "onnxruntime>=1.15.0",
        "scipy>=1.10.0",
        "sympy>=1.12",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
        "packaging>=23.0",
        "requests>=2.31.0",
    ]
    
    # Install requirements
    install_result = install_requirements(venv_path, requirements)
    if install_result.is_err():
        raise Exception(f"Failed to install requirements: {install_result.unwrap_err()}")
    
    print(f"Successfully installed verinet with venv at {install_dir}")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate") 