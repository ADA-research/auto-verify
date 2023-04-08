"""TODO summary."""
from result import Err, Ok, Result
from xdg_base_dirs import xdg_data_home

XDG_DATA_HOME = xdg_data_home()
AV_HOME = XDG_DATA_HOME / "autoverify"


def _install_verifier(verifier: str) -> Result[None, str]:
    """_summary_."""
    if verifier == "DummyVerifier":
        # Do some installing, and if it all goes well:
        return Ok()

    return Err("Oops")


# TODO: Real logging, not prints
def try_install_verifiers(verifiers: list[str]):
    """_summary_."""
    for verifier in verifiers:
        print(f"Installing {verifier}...")

        install_result = _install_verifier(verifier)

        if isinstance(install_result, Ok):
            print(f"Succesfully installed {verifier}")
        elif isinstance(install_result, Err):
            print(f"Error installing {verifier}: \n{install_result.err()}")
