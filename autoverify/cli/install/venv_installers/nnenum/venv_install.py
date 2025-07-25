"""nnenum venv-based installer."""

from pathlib import Path

from autoverify.cli.install.venv_installers.venv_install import (
    create_verifier_venv,
    install_requirements,
)
from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier

VenvNnenumRepoInfo = GitRepoInfo(
    branch="vnncomp2022",
    commit_hash="c68562d",
    clone_url="https://github.com/kw-corne/nnenum",
)


def install(install_dir: Path):
    """
    Installs nnenum using virtual environment and uv/pip.

    Args:
        install_dir: Path where nnenum is installed.
    """
    # Clone the repository
    clone_checkout_verifier(VenvNnenumRepoInfo, install_dir)
    
    # Create virtual environment
    venv_result = create_verifier_venv(install_dir)
    if venv_result.is_err():
        raise Exception(f"Failed to create venv: {venv_result.unwrap_err()}")
        
    venv_path = venv_result.unwrap()
    
    # Define requirements for nnenum
    requirements = [
        "numpy==1.23.2",
        "onnx==1.12.0",
        "onnxruntime==1.12.1",
        "scikit-learn==1.2.2",
        "scipy==1.9.0",
        "swiglpk==5.0.8",
        "sympy==1.11.1",
        "coloredlogs==15.0.1",
        "termcolor==2.2.0",
        "requests==2.28.2",
        "joblib==1.2.0",
        "mpmath==1.3.0",
    ]
    
    # Install requirements
    install_result = install_requirements(venv_path, requirements)
    if install_result.is_err():
        raise Exception(f"Failed to install requirements: {install_result.unwrap_err()}")
    
    print(f"Successfully installed nnenum with venv at {install_dir}")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate") 