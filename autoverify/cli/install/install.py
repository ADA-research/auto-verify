from pathlib import Path

from result import Err, Ok, Result
from xdg_base_dirs import xdg_data_home

XDG_DATA_HOME = xdg_data_home()
AV_HOME = XDG_DATA_HOME / "auto_verify"


def install_verifiers(verifiers: list[str]) -> Result[list[str], str]:
    """Install one or more specified verifiers."""
    return Ok(["testlalalala"])
