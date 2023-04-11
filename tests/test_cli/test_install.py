"""_summary_."""
import subprocess

import pytest

from autoverify import __version__ as AV_VERSION


def run_av_cli(args: list[str]) -> str:
    base_cmd = ["auto-verify"]
    base_cmd.extend(args)

    result = subprocess.run(base_cmd, stdout=subprocess.PIPE)
    return str(result.stdout)


def test_version():
    output = run_av_cli(["--version"])
    assert output.find(AV_VERSION) >= 0


def test_no_args():
    """No args should show the help menu."""
    output = run_av_cli([])
    assert output.find("usage: auto-verify") >= 0


def test_install(monkeypatch: pytest.MonkeyPatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    output = run_av_cli(["--install", "DummyVerifier"])

    assert output.find("Succesfully installed") >= 0
