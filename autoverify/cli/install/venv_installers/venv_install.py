"""
Virtual environment based installation for auto-verify verifiers.

This module provides functionality to install verifiers using Python virtual
environments and uv package manager instead of conda.
"""

import logging
import os
import shutil
import subprocess
from collections.abc import Iterable
from pathlib import Path
from subprocess import CalledProcessError
from typing import Optional

from result import Err, Ok, Result
from xdg_base_dirs import xdg_data_home

VENV_AV_HOME = xdg_data_home() / "autoverify-venv"
VENV_VERIFIER_DIR = VENV_AV_HOME / "verifiers"
TOOL_DIR_NAME = "tool"
VENV_DIR_NAME = "venv"


def _create_base_dirs():
    """Creates the venv-based directory structure."""
    VENV_VERIFIER_DIR.mkdir(parents=True, exist_ok=True)


def _remove_verifier_dir(verifier: str):
    """Removes the directory associated with the verifier."""
    print(f"Removing venv-based {verifier} directory")
    shutil.rmtree(VENV_VERIFIER_DIR / verifier)


def _init_new_verifier_dir(dir_name: str) -> Result[None, str]:
    """Creates a new directory in `VENV_VERIFIER_DIR` with specified name.
    
    Args:
        dir_name: Name of the verifier directory to create
        
    Returns:
        Result indicating success or an error message
    """
    dir_path = VENV_VERIFIER_DIR / dir_name
    
    if dir_path.exists():
        return Err(f"Verifier '{dir_name}' is already installed at {dir_path}")
        
    try:
        dir_path.mkdir()
        return Ok()
    except Exception as err:
        return Err(f"Failed to create directory for {dir_name}: {err}")


def _check_uv_available() -> bool:
    """Check if uv is available in the system."""
    try:
        result = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, check=True
        )
        logging.info(f"uv version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _create_venv_with_uv(venv_path: Path, venv_name: str) -> Result[None, str]:
    """Create a virtual environment using uv.
    
    Args:
        venv_path: Path where the venv will be created
        venv_name: Name for the virtual environment
    """
    try:
        cmd = ["uv", "venv", str(venv_path), "--name", f"autoverify-{venv_name}"]
        subprocess.run(cmd, check=True, capture_output=True)
        logging.info(f"Created virtual environment at {venv_path}")
        return Ok()
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        logging.error(f"Failed to create venv with uv: {error_msg}")
        return Err(f"uv venv creation failed: {error_msg}")


def _create_venv_fallback(venv_path: Path, venv_name: str) -> Result[None, str]:
    """Fallback to standard venv if uv is not available.
    
    Args:
        venv_path: Path where the venv will be created
        venv_name: Name for the virtual environment
    """
    try:
        import venv
        venv.create(venv_path, with_pip=True, prompt=f"autoverify-{venv_name}")
        logging.info(f"Created virtual environment at {venv_path} (fallback)")
        return Ok()
    except Exception as e:
        logging.error(f"Failed to create venv with fallback: {e}")
        return Err(f"Fallback venv creation failed: {str(e)}")


def create_verifier_venv(verifier_dir: Path, verifier_name: str) -> Result[Path, str]:
    """
    Create a virtual environment for the verifier.
    
    Args:
        verifier_dir: Directory where the verifier will be installed
        verifier_name: Name of the verifier
        
    Returns:
        Result containing the venv path or error message
    """
    venv_path = verifier_dir / VENV_DIR_NAME
    
    # Try uv first, fallback to standard venv
    if _check_uv_available():
        result = _create_venv_with_uv(venv_path, verifier_name)
    else:
        logging.warning("uv not found, falling back to standard venv")
        result = _create_venv_fallback(venv_path, verifier_name)
    
    if isinstance(result, Ok):
        return Ok(venv_path)
    else:
        return result


def install_requirements_with_uv(venv_path: Path, requirements: list[str]) -> Result[None, str]:
    """
    Install requirements using uv.
    
    Args:
        venv_path: Path to the virtual environment
        requirements: List of requirements to install
        
    Returns:
        Result indicating success or failure
    """
    try:
        cmd = ["uv", "pip", "install", "--python", str(venv_path / "bin" / "python")] + requirements
        subprocess.run(cmd, check=True, capture_output=True)
        logging.info(f"Installed requirements with uv: {requirements}")
        return Ok()
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        logging.error(f"Failed to install requirements with uv: {error_msg}")
        return Err(f"uv pip install failed: {error_msg}")


def install_requirements_fallback(venv_path: Path, requirements: list[str]) -> Result[None, str]:
    """
    Install requirements using standard pip.
    
    Args:
        venv_path: Path to the virtual environment
        requirements: List of requirements to install
        
    Returns:
        Result indicating success or failure
    """
    try:
        pip_path = venv_path / "bin" / "pip"
        cmd = [str(pip_path), "install"] + requirements
        subprocess.run(cmd, check=True, capture_output=True)
        logging.info(f"Installed requirements with pip: {requirements}")
        return Ok()
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        logging.error(f"Failed to install requirements with pip: {error_msg}")
        return Err(f"pip install failed: {error_msg}")


def install_requirements(venv_path: Path, requirements: list[str]) -> Result[None, str]:
    """
    Install requirements using the best available method.
    
    Args:
        venv_path: Path to the virtual environment
        requirements: List of requirements to install
        
    Returns:
        Result indicating success or failure
    """
    if _check_uv_available():
        return install_requirements_with_uv(venv_path, requirements)
    else:
        return install_requirements_fallback(venv_path, requirements)


def get_venv_python_path(verifier: str) -> Path:
    """Get the path to the Python executable in the verifier's venv."""
    return VENV_VERIFIER_DIR / verifier / VENV_DIR_NAME / "bin" / "python"


def get_venv_activation_cmd(verifier: str) -> str:
    """Get the command to activate the verifier's venv."""
    activate_path = VENV_VERIFIER_DIR / verifier / VENV_DIR_NAME / "bin" / "activate"
    return f"source {activate_path}"


def _uninstall_verifier_venv(verifier: str) -> Result[None, str]:
    """Tries to uninstall the specified verifier."""
    verifier_path = VENV_VERIFIER_DIR / verifier
    
    if not verifier_path.exists():
        return Err(f"Verifier '{verifier}' is not installed (path {verifier_path} does not exist)")
        
    try:
        _remove_verifier_dir(verifier)
        return Ok()
    except Exception as err:
        print(f"Error removing verifier directory: {err}")
        return Err(f"Exception when deleting verifier directory: {err}")


def _install_verifier_venv(verifier: str, installer_func, custom_commit: Optional[str] = None, use_latest: bool = False) -> Result[None, str]:
    """Tries to install the specified verifier.
    
    Args:
        verifier: Name of the verifier to install
        installer_func: Function to install the verifier
        custom_commit: Optional specific commit hash to checkout
        use_latest: If True, checkout the latest commit on the branch
        
    Returns:
        Result indicating success or failure
    """
    # Create the verifier directory
    init_result = _init_new_verifier_dir(verifier)
    if init_result.is_err():
        return init_result

    dir_path = VENV_VERIFIER_DIR / verifier

    try:
        # Pass version information to the installer
        installer_func(dir_path, custom_commit=custom_commit, use_latest=use_latest)
        
        # Create activation script
        with open(dir_path / "activate.sh", "w") as f:
            f.write(f"#!/bin/bash\nsource {dir_path / VENV_DIR_NAME / 'bin' / 'activate'}\n")
        
        # Make the activation script executable
        os.chmod(dir_path / "activate.sh", 0o755)
        
        return Ok()
    except Exception as err:
        if isinstance(err, CalledProcessError):
            err = err.stderr.decode("utf-8")

        logging.exception(err)
        _remove_verifier_dir(verifier)
        return Err(f"Exception during installation: {err}")


def try_install_verifiers_venv(verifiers: Iterable[str], installers: dict, version: Optional[str] = None):
    """Tries to install the specified verifiers.

    Will print the result of each attempt to stdout.

    Args:
        verifiers: Names of the verifiers to install.
        installers: Dictionary mapping verifier names to installer functions.
        version: Optional version specifier (commit hash or "most-recent")
    """
    _create_base_dirs()

    for verifier in verifiers:
        print(f"\nInstalling {verifier} with venv...")
        
        if verifier not in installers:
            print(f"Error: No venv installer found for verifier {verifier}")
            continue
            
        if version:
            print(f"Using version: {version}")
            
        use_latest = version == "most-recent"
        custom_commit = None if use_latest else version

        install_result = _install_verifier_venv(
            verifier, installers[verifier], custom_commit=custom_commit, use_latest=use_latest
        )

        if isinstance(install_result, Ok):
            print(f"Successfully installed {verifier} with venv")
            print(f"To activate: source {VENV_VERIFIER_DIR / verifier / 'activate.sh'}")
        elif isinstance(install_result, Err):
            print(f"Error installing {verifier}: {install_result.err()}")


def try_uninstall_verifiers_venv(verifiers: Iterable[str]):
    """Tries to uninstall the specified verifiers.

    Will print the result of each attempt to stdout.

    Args:
        verifiers: Names of the verifiers to uninstall.
    """
    for verifier in verifiers:
        print(f"\nUninstalling venv-based {verifier}...")

        uninstall_result = _uninstall_verifier_venv(verifier)

        if isinstance(uninstall_result, Ok):
            print(f"Successfully uninstalled venv-based {verifier}")
        elif isinstance(uninstall_result, Err):
            print(f"Error uninstalling venv-based {verifier}: {uninstall_result.err()}") 