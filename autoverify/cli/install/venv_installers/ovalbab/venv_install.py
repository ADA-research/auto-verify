"""ovalbab venv installer."""

from pathlib import Path

from result import Ok

from autoverify.cli.install.venv_installers.venv_install import (
    create_verifier_venv,
    install_requirements,
)
from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier

VenvOvalBabRepoInfo = GitRepoInfo(
    branch="main",
    commit_hash="5de3113",
    clone_url="https://github.com/oval-group/oval-bab",
)


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs ovalbab with venv.

    Args:
        install_dir: Path where oval-bab is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository
    clone_checkout_verifier(VenvOvalBabRepoInfo, install_dir, custom_commit=custom_commit, use_latest=use_latest)

    # Create virtual environment
    venv_result = create_verifier_venv(install_dir, "ovalbab")
    venv_path = venv_result.unwrap()

    # Create requirements file reflecting conda environment
    requirements_file = install_dir / "requirements.txt"
    with open(requirements_file, "w") as f:
        f.write("""# Critical pinned packages (matching conda environment)
python>=3.8,<3.9
torch==2.0.0
torchvision==0.15.0
torchaudio==2.0.0
numpy==1.24.3
sympy==1.11.1

# Core scientific computing
scipy>=1.7.0
matplotlib>=3.5.0
mpmath>=1.3.0
networkx>=2.8.0

# Deep learning and ML
torch-cuda>=2.0.0
torchtriton>=2.0.0

# Data processing and utilities
requests>=2.28.0
urllib3>=1.26.0
certifi>=2022.0.0
charset-normalizer>=3.0.0
idna>=3.4
six>=1.16.0
setuptools>=68.0.0
wheel>=0.40.0
pip>=23.0.0

# Image processing
pillow>=9.0.0
imageio>=2.15.0
tifffile>=2022.0.0

# System and crypto
cryptography>=3.4.0
cffi>=1.14.0
pycparser>=2.20.0
pyopenssl>=22.0.0
pysocks>=1.7.0

# Intel optimizations
intel-openmp

# Development and testing
pytest>=7.0.0
pytest-cov>=4.0.0
coverage>=7.0.0
black>=23.0.0
flake8>=6.0.0

# Additional dependencies
jinja2>=3.1.0
markupsafe>=2.1.0
typing-extensions>=4.0.0
""")

    # Install the package itself
    requirements = [
        "-r",
        str(requirements_file),
        "-e",
        str(install_dir / "tool"),  # Install in development mode
    ]
    install_requirements(venv_path, requirements)

    # Print installation information
    print("\nOVALBAB (venv) Installation Complete")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")

    return Ok()
