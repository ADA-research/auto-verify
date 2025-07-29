"""nnenum venv installer."""

import os
import shutil
from pathlib import Path
from typing import Optional

from result import Ok

from autoverify.cli.install.venv_installers.venv_install import (
    create_verifier_venv,
    install_requirements,
)
from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier
from autoverify.util.env import cwd

VenvNnenumRepoInfo = GitRepoInfo(
    branch="master",
    commit_hash="e9c0b0a",
    clone_url="https://github.com/stanleybak/nnenum",
)


def install(install_dir: Path, custom_commit: Optional[str] = None, use_latest: bool = False):
    """Installs nnenum with venv.

    Args:
        install_dir: Path where nnenum is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository
    clone_checkout_verifier(
        VenvNnenumRepoInfo, 
        install_dir, 
        custom_commit=custom_commit, 
        use_latest=use_latest
    )
    
    # Create virtual environment
    venv_result = create_verifier_venv(install_dir, "nnenum")
    venv_path = venv_result.unwrap()
    
    # Define requirements
    requirements = [
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.5.0",
        "onnx>=1.12.0",
        "onnxruntime>=1.12.0",
        "torch>=1.11.0",
        "termcolor>=2.0.0",
        "pytest>=7.0.0",
        "pillow>=9.0.0",
    ]
    
    # Install requirements
    install_result = install_requirements(venv_path, requirements)
    
    # Print installation information
    print("\nNNENUM (venv) Installation Complete")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")
    
    return Ok() 