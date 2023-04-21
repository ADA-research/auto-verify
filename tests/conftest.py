import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--nn_props",
        action="store_true",
        default=False,
        help="run property tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "nn_prop: mark test as nn prop tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--nn_props"):
        return

    skip_install = pytest.mark.skip(reason="need --nn_props option to run")

    for item in items:
        if "nn_prop" in item.keywords:
            item.add_marker(skip_install)
