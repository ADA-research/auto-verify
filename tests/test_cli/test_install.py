"""_summary_."""
import subprocess

from autoverify import __version__ as AV_VERSION


def test_version():
    """Also serves as a test to see if the CLI works at all."""
    result = subprocess.run(
        ["auto-verify", "--version"], stdout=subprocess.PIPE
    )
    assert str(result.stdout).find(AV_VERSION) >= 0
