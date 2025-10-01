"""Nnenum venv installer."""

from pathlib import Path

from result import Ok

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


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs nnenum with venv.

    Args:
        install_dir: Path where nnenum is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository
    clone_checkout_verifier(VenvNnenumRepoInfo, install_dir, custom_commit=custom_commit, use_latest=use_latest)

    # Create virtual environment
    venv_result = create_verifier_venv(install_dir, "nnenum")
    venv_path = venv_result.unwrap()

    # Create requirements file reflecting conda environment
    requirements_file = install_dir / "requirements.txt"
    with open(requirements_file, "w") as f:
        f.write("""# Critical pinned packages (matching conda environment)
numpy==1.23.2
onnx==1.12.0
onnxruntime==1.12.1
onnxconverter-common==1.13.0

# Core scientific computing
scipy==1.9.0
scikit-learn==1.2.2
mpmath==1.3.0
sympy==1.11.1

# Data processing and utilities
absl-py==1.4.0
charset-normalizer==3.1.0
coloredlogs==15.0.1
humanfriendly==10.0
idna==3.4
joblib==1.2.0
requests==2.28.2
urllib3==1.26.15
termcolor==2.2.0
threadpoolctl==3.1.0

# ONNX ecosystem
flatbuffers==23.3.3
skl2onnx==1.12

# Linear programming
swiglpk==5.0.8

# Development and testing
pytest>=7.0.0
pytest-cov>=4.0.0
coverage>=7.0.0
black>=23.0.0
flake8>=6.0.0

# System utilities
setuptools>=68.0.0
wheel>=0.40.0
pip>=23.0.0
""")

    # Install requirements
    requirements = ["-r", str(requirements_file)]
    install_requirements(venv_path, requirements)

    # Print installation information
    print("\nNNENUM (venv) Installation Complete")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")

    return Ok()
