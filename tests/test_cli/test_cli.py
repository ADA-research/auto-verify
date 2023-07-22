"""_summary_."""
# TODO: Dont hardcore error strings, import them from somewhere instead
import subprocess

import autoverify


def run_av_cli(args: list[str]) -> str:
    base_cmd = ["auto-verify"]
    base_cmd.extend(args)

    result = subprocess.run(base_cmd, stdout=subprocess.PIPE)
    return str(result.stdout)


def test_version():
    output = run_av_cli(["--version"])
    assert output.find(autoverify.__version__) >= 0


def test_no_args():
    """No args should show the help menu."""
    output = run_av_cli([])
    assert output.find("usage: auto-verify") >= 0
