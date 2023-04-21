"""_summary_."""
# TODO: Dont hardcore error strings, import them from somewhere instead
import autoverify
from tests.util import run_av_cli


def test_version():
    output = run_av_cli(["--version"])
    assert output.find(autoverify.__version__) >= 0


def test_no_args():
    """No args should show the help menu."""
    output = run_av_cli([])
    assert output.find("usage: auto-verify") >= 0
