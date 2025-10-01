"""verinet venv installer."""

from pathlib import Path

from result import Ok

from autoverify.cli.install.venv_installers.venv_install import (
    create_verifier_venv,
    install_requirements,
)
from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier

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
    
    # Create requirements file reflecting conda environment
    requirements_file = install_dir / "requirements.txt"
    with open(requirements_file, "w") as f:
        f.write("""# Critical pinned packages (matching conda environment)
numpy==1.21.6
onnx==1.10.2
onnxruntime==1.15.1
torch==2.0.1
torchvision==0.15.2
tensorflow==2.7.4
tensorflow-estimator==2.7.0

# Core scientific computing
scipy==1.10.1
matplotlib==3.7.1
mpmath==1.3.0
sympy==1.12
networkx==3.1

# Deep learning and ML
keras==2.7.0
keras-preprocessing==1.1.2
tensorboard==2.13.0
tensorboard-data-server==0.7.1
tensorflow-io-gcs-filesystem==0.32.0

# ONNX ecosystem
opt-einsum==3.3.0

# Data processing and utilities
requests==2.31.0
urllib3==1.26.16
certifi==2023.5.7
charset-normalizer==3.1.0
idna==3.4
six==1.16.0
setuptools==68.0.0
wheel==0.40.0
pip>=23.0.0

# Image processing
pillow==9.5.0
imageio==2.31.1
tifffile==2023.4.12
scikit-image==0.18.3
pywavelets==1.4.1

# Google ecosystem
absl-py==1.4.0
google-auth==2.21.0
google-auth-oauthlib==1.0.0
google-pasta==0.2.0
grpcio==1.56.0
protobuf==3.19.6

# Configuration and optimization
configspace==0.7.1
cachetools==5.3.1
astunparse==1.6.3
cmake==3.26.4

# Neural network verification
dnnv==0.6.0

# Development and testing
pytest>=7.0.0
pytest-cov>=4.0.0
coverage>=7.0.0
black>=23.0.0
flake8>=6.0.0

# Additional dependencies
termcolor==2.3.0
tqdm==4.65.0
triton==2.0.0
typing-extensions==4.6.3
werkzeug==2.3.6
wrapt==1.15.0
xpress==9.1.2
zipp==3.15.0
lark==1.1.5
libclang==16.0.0
lit==16.0.6
netron==7.8.6
oauthlib==3.2.2
pyasn1==0.5.0
pyasn1-modules==0.3.0
pyparsing==3.1.0
python-dateutil==2.8.2
rsa==4.9
""")

    # Install requirements
    requirements = ["-r", str(requirements_file)]
    install_requirements(venv_path, requirements)
    
    # Print installation information
    print("\nVERINET (venv) Installation Complete")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")
    
    return Ok() 