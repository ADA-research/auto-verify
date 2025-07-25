from pathlib import Path

import pytest
from autoverify.cli.install.install import try_install_verifiers
from pytest import CaptureFixture, MonkeyPatch


@pytest.fixture
def mock_verifier_dir(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr("autoverify.cli.install.install.VERIFIER_DIR", tmp_path)


def test_bad_install(mock_verifier_dir, capfd: CaptureFixture):
    test_name = "_test_verifier_that_doesnt_exist"
    try_install_verifiers([test_name])

    captured = capfd.readouterr()
    assert (
        f"Error installing {test_name}: "
        f"No installer found for verifier {test_name}" in captured.out
    )
