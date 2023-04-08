"""TODO summary."""
from result import Err, Ok, Result
from xdg_base_dirs import xdg_data_home

XDG_DATA_HOME = xdg_data_home()
AV_HOME = XDG_DATA_HOME / "autoverify"


def install_verifier(verifier: str) -> Result[None, str]:
    """_summary_."""
    if verifier == "DummyVerifier":
        return Ok()

    return Err("Unknown verifier")


def try_install_verifiers(verifiers: list[str]):
    """_summary_."""
    for verifier in verifiers:
        install_result = install_verifier(verifier)
