"""abcrown venv installer."""

from pathlib import Path

from result import Ok

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


def install(install_dir: Path, custom_commit: str | None = None, use_latest: bool = False):
    """Installs abcrown with venv.

    Args:
        install_dir: Path where ab-crown is installed.
        custom_commit: Optional specific commit hash to checkout.
        use_latest: If True, checkout the latest commit on the branch.
    """
    # Clone and checkout the repository
    clone_checkout_verifier(
        VenvAbCrownRepoInfo, 
        install_dir, 
        custom_commit=custom_commit, 
        use_latest=use_latest
    )
    
    # Create virtual environment
    venv_result = create_verifier_venv(install_dir, "abcrown")
    venv_path = venv_result.unwrap()
    
    # Create requirements file reflecting conda environment
    requirements_file = install_dir / "requirements.txt"
    with open(requirements_file, "w") as f:
        f.write("""# Critical pinned packages (matching conda environment)
numpy==1.21.5
pandas==1.3.4
torch==1.11.0
torchvision==0.12.0
torchaudio==0.12.0
tensorboard
tensorboard-data-server
tensorboard-plugin-wit
tensorflow
tensorflow-estimator
tensorflow-base

# Core scientific computing
scipy>=1.7.3
matplotlib>=3.5.1
h5py>=3.1.0
scikit-image>=0.18.0

# Deep learning and ML
keras>=2.9.0
keras-preprocessing>=1.1.2
onnx==1.11.0
onnxruntime==1.11.0
onnxoptimizer==0.3.13
onnx2pytorch @ git+https://github.com/KaidiXu/onnx2pytorch@102cf22e64ea7fae9462c1ba0feaa250ac0bc628#egg=onnx2pytorch

# Data processing and utilities
pyyaml>=6.0
tqdm>=4.64.0
appdirs>=1.4.4
requests>=2.28.0
urllib3>=1.26.0
certifi>=2022.0.0
charset-normalizer>=3.0.0
idna>=3.4
six>=1.16.0

# Image processing
pillow>=9.0.0
imageio>=2.15.0
tifffile>=2022.0.0

# Network and async
aiohttp>=3.8.0
aiosignal>=1.2.0
async-timeout>=4.0.0
asynctest>=0.13.0
frozenlist>=1.3.0
multidict>=6.0.0
yarl>=1.7.0

# Google ecosystem
absl-py>=1.4.0
google-auth>=2.18.0
google-auth-oauthlib>=0.4.6
google-pasta>=0.2.0
grpcio>=1.54.0
protobuf==3.20.1

# Configuration and serialization
attrs>=23.0.0
click>=8.1.0
configobj>=5.0.6
jsonschema>=3.2.0
toml>=0.10.2
tomli>=2.0.1

# Visualization
graphviz>=0.20.0

# Development and testing
pytest>=7.0.0
pytest-cov>=4.0.0
coverage>=7.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0

# System utilities
psutil>=5.9.0
setuptools>=68.0.0
wheel>=0.40.0
pip>=23.0.0

# Intel optimizations
intel-openmp

# Additional dependencies
flatbuffers==2.0
termcolor>=2.0.0
werkzeug>=2.2.0
jinja2>=3.1.0
markupsafe>=2.1.0
""")

    # Install requirements
    requirements = ["-r", str(requirements_file)]
    install_requirements(venv_path, requirements)
    
    # Print installation information
    print("\nABCROWN (venv) Installation Complete")
    print(f"Virtual environment: {venv_path}")
    print(f"To activate: source {venv_path}/bin/activate")
    print("To use: python -m abcrown.main --config CONFIG_FILE")
    
    return Ok() 