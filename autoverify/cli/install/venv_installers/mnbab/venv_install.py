"""mnbab venv installer."""

from pathlib import Path

from result import Ok

from autoverify.cli.install.venv_installers.venv_install import (
    create_verifier_venv,
    install_requirements,
)
from autoverify.cli.util.git import GitRepoInfo, clone_checkout_verifier

VenvMnBabRepoInfo = GitRepoInfo(
    branch="SABR_ready",
    commit_hash="70751b8",
    clone_url="https://github.com/eth-sri/mn-bab",
)


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs mnbab with venv.

    Args:
        install_dir: Path where mn-bab is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository
    clone_checkout_verifier(
        VenvMnBabRepoInfo, 
        install_dir, 
        custom_commit=custom_commit, 
        use_latest=use_latest,
        init_submodules=True
    )
    
    # Create virtual environment
    venv_result = create_verifier_venv(install_dir, "mnbab")
    venv_path = venv_result.unwrap()
    
    # Create requirements file reflecting conda environment
    requirements_file = install_dir / "requirements.txt"
    with open(requirements_file, "w") as f:
        f.write("""# Critical pinned packages (matching conda environment)
gurobipy==9.1.2

# Core scientific computing
numpy==1.21.0
scipy>=1.7.0
matplotlib==3.5.3
h5py==3.8.0

# Deep learning and ML
keras==2.9.0
keras-preprocessing==1.1.2
tensorflow==2.9.1
tensorflow-estimator==2.9.0
tensorboard==2.9.1
tensorboard-data-server==0.6.1
tensorboard-plugin-wit==1.8.1
torch==1.11.0
torchvision==0.12.0
mxnet==1.9.1

# ONNX ecosystem
onnx==1.11.0
onnxruntime==1.11.0
opt-einsum==3.3.0

# Data processing and utilities
pandas==1.2.5
pyyaml==5.4.1
tqdm==4.65.0
appdirs==1.4.4
requests==2.30.0
urllib3==1.26.15
certifi>=2022.0.0
charset-normalizer==3.1.0
idna==3.4
six==1.16.0

# Image processing
pillow==9.1.1
imageio>=2.15.0

# Google ecosystem
absl-py==1.4.0
google-auth==2.18.0
google-auth-oauthlib==0.4.6
google-pasta==0.2.0
grpcio==1.54.2
protobuf==3.19.6

# Configuration and serialization
attrs==23.1.0
click==8.1.3
configobj==5.0.6
jsonschema==3.2.0
toml==0.10.2
tomli==2.0.1
python-box==6.1.0
python-dateutil==2.8.2
pytz==2023.3

# Development and testing
pytest==7.3.1
pytest-cov==4.0.0
coverage==7.2.5
black==23.3.0
flake8>=6.0.0
mypy-extensions==0.4.3
pre-commit==2.20.0

# System utilities
psutil>=5.9.0
setuptools>=68.0.0
wheel>=0.40.0
pip>=23.0.0
virtualenv==20.4.7

# Additional dependencies
flatbuffers==1.12
termcolor==2.3.0
werkzeug==2.2.3
jinja2>=3.1.0
markupsafe==2.1.2
markdown==3.4.3
gast==0.4.0
libclang==16.0.0
nvidia-ml-py3==7.352.0
websocket-client==1.3.3
wrapt==1.15.0
wurlitzer==3.0.3

# ELINA dependencies (for mnbab)
# Note: These are system-level dependencies that may need to be installed separately
# - cddlib
# - gmp
# - mpfr
""")

    # Install requirements
    requirements = ["-r", str(requirements_file)]
    install_requirements(venv_path, requirements)
    
    # Create deps directory (similar to conda installer)
    deps_dir = install_dir / "deps"
    deps_dir.mkdir(exist_ok=True)
    
    # Note: ELINA compilation would need to be handled separately in venv mode
    # as it requires system-level dependencies and compilation tools
    
    # Print installation information
    print("\nMNBAB (venv) Installation Complete")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")
    print("Note: ELINA compilation may require additional system dependencies")
    
    return Ok()
