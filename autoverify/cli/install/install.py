"""TODO summary."""
# TODO: Logging instead of prints
import shutil

from result import Err, Ok, Result
from xdg_base_dirs import xdg_data_home

from .installers import installers

AV_HOME = xdg_data_home() / "autoverify"
VERIFIER_DIR = AV_HOME / "verifiers"


def _create_base_dirs():
    """Creates the XDG_DATA_HOME/autoverify/verifiers directories."""
    AV_HOME.mkdir(exist_ok=True)
    VERIFIER_DIR.mkdir(exist_ok=True)


def _remove_verifier_dir(verifier: str):
    """_summary_."""
    print("Removing verifier directory")
    shutil.rmtree(VERIFIER_DIR / verifier, ignore_errors=True)


def _init_new_verifier_dir(dir_name: str):
    """_summary_."""
    dir_path = VERIFIER_DIR / dir_name
    dir_path.mkdir()

    (dir_path / "venv").mkdir()
    (dir_path / "tool").mkdir()


def _install_verifier(verifier: str) -> Result[None, str]:
    """_summary_."""
    if verifier not in installers:
        return Err(f"No installer found for verifier {verifier}")

    try:
        _init_new_verifier_dir(verifier)
    except Exception as err:
        print(f"Error initializing new verifier directory: {err=}")
        return Err("Directory initialization failed")

    dir_path = VERIFIER_DIR / verifier / "tool"

    try:
        installers[verifier](dir_path)
        return Ok()
    except Exception as err:
        print(f"Error installing verifier: {err=}")
        _remove_verifier_dir(verifier)
        return Err("Exception during installation")


def try_install_verifiers(verifiers: list[str]):
    """_summary_."""
    _create_base_dirs()

    for verifier in verifiers:
        print(f"Installing {verifier}...")

        install_result = _install_verifier(verifier)

        if isinstance(install_result, Ok):
            print(f"Succesfully installed {verifier}")
        elif isinstance(install_result, Err):
            print(f"Error installing {verifier}: {install_result.err()}")
