"""_summary_."""
# TODO: Dont hardcore error strings, import them from somewhere instead
import subprocess
from pathlib import Path

import pytest

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


def test_install(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    output = run_av_cli(["--install", "DummyVerifier"])

    assert output.find("Succesfully installed") >= 0

    # Installing the same verifier twice should fail
    output = run_av_cli(["--install", "DummyVerifier"])
    assert output.find("Error initializing") >= 0


# TODO: Needs proper cleanup mechanisms, very wonky atm.
def test_install_nnenum(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    output = run_av_cli(["--install", "nnenum"])

    assert output.find("Succesfully installed") >= 0

    output = run_av_cli(["--uninstall", "nnenum"])

    assert output.find("Succesfully uninstalled") >= 0
