"""abcrown venv-based installer."""

from pathlib import Path

from autoverify.cli.install.venv_installers.venv_install import (
    create_verifier_venv,
    install_requirements,
)
from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier

VenvAbCrownRepoInfo = GitRepoInfo(
    branch="main", 
    commit_hash="877afa32d9d314fcb416436a616e6a5878fdab78",
    clone_url="https://github.com/Verified-Intelligence/alpha-beta-CROWN",
)


def install(install_dir: Path):
    """
    Installs abcrown using virtual environment and uv/pip.

    Args:
        install_dir: Path where abcrown is installed.
    """
    # Clone the repository
    clone_checkout_verifier(VenvAbCrownRepoInfo, install_dir)
    
    # Create virtual environment  
    venv_result = create_verifier_venv(install_dir)
    if venv_result.is_err():
        raise Exception(f"Failed to create venv: {venv_result.unwrap_err()}")
        
    venv_path = venv_result.unwrap()
    
    # Define requirements for abcrown (simplified from conda env)
    requirements = [
        # Core dependencies
        "torch>=2.0.0",
        "torchvision", 
        "numpy>=1.24.0",
        "onnx>=1.13.0",
        "onnxruntime>=1.15.0",
        "scipy>=1.10.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0",
        "psutil>=5.9.0",
        "tqdm>=4.65.0",
        "packaging>=23.0",
        "coloredlogs>=15.0",
        # Additional dependencies that can be installed via pip
        "pillow>=10.0.0",
        "requests>=2.31.0",
        "matplotlib",
        "sympy>=1.12",
    ]
    
    # Install requirements
    install_result = install_requirements(venv_path, requirements)
    if install_result.is_err():
        raise Exception(f"Failed to install requirements: {install_result.unwrap_err()}")
    
    print(f"Successfully installed abcrown with venv at {install_dir}")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")
    print("Note: This is a simplified installation. Some advanced features may require additional dependencies.") 