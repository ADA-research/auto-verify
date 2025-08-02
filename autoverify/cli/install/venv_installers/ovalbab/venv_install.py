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
    clone_checkout_verifier(
        VenvOvalBabRepoInfo, 
        install_dir, 
        custom_commit=custom_commit, 
        use_latest=use_latest
    )
    
    # Create virtual environment
    venv_result = create_verifier_venv(install_dir, "ovalbab")
    venv_path = venv_result.unwrap()
    
    # Create requirements file
    requirements_file = install_dir / "requirements.txt"
    with open(requirements_file, "w") as f:
        f.write("""
numpy>=1.21.0
torch>=1.11.0
torchvision>=0.12.0
scipy>=1.7.3
matplotlib>=3.5.1
pyyaml>=6.0
tqdm>=4.64.0
onnx>=1.12.0
onnxruntime>=1.12.1
appdirs>=1.4.4
""")

    # Install the package itself
    requirements = [
        "-r", str(requirements_file),
        "-e", str(install_dir / "tool")  # Install in development mode
    ]
    install_requirements(venv_path, requirements)
    
    # Print installation information
    print("\nOVALBAB (venv) Installation Complete")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")
    
    return Ok()