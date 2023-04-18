import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--runinstall",
        action="store_true",
        default=False,
        help="run install tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "install: mark test as installs")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runinstall"):
        return

    skip_install = pytest.mark.skip(reason="need --runinstall option to run")

    for item in items:
        if "install" in item.keywords:
            item.add_marker(skip_install)
