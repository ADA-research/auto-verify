import json
from pathlib import Path

import pytest
from ConfigSpace import Configuration, ConfigurationSpace

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio


@pytest.fixture
def pf_cfg(simple_configspace: ConfigurationSpace) -> Configuration:
    return simple_configspace.sample_configuration()


@pytest.fixture
def pf_cfg2(simple_configspace: ConfigurationSpace) -> Configuration:
    return simple_configspace.sample_configuration()


@pytest.fixture
def portfolio(pf_cfg: Configuration, pf_cfg2: Configuration) -> Portfolio:
    pf = Portfolio()
    pf.add(ConfiguredVerifier("foo", pf_cfg))
    pf.add(ConfiguredVerifier("hello", pf_cfg2, resources=(8, 1)))
    pf.update_costs({"bar": 42.0})
    pf.update_costs({"foobar": 7.0})

    return pf


@pytest.fixture
def portfolio_json(portfolio: Portfolio, tmpdir: Path) -> Path:
    json_path = tmpdir / "pf.json"
    portfolio.to_json(json_path)
    return json_path


def test_get_cost(portfolio: Portfolio):
    cost = portfolio.get_cost("bar")
    assert cost == 42.0

    costs = portfolio.get_costs(["bar", "foobar"])
    assert costs == {"bar": 42.0, "foobar": 7.0}

    with pytest.raises(KeyError):
        portfolio.get_cost("hello world")


def test_to_json(portfolio: Portfolio, tmpdir: Path):
    portfolio.to_json(tmpdir / "pf.json")

    with open(tmpdir / "pf.json") as f:
        pf_json = json.load(f)

    assert len(pf_json) == 2

    seen = {
        "foo": False,
        "hello": False,
    }

    for cv in pf_json:
        if cv["verifier"] == "foo":
            seen["foo"] = True
        elif cv["verifier"] == "hello":
            seen["hello"] = True

    assert all(v for v in seen.values())


def test_from_json(
    portfolio_json: Path, simple_configspace: ConfigurationSpace
):
    cfg_space_map = {
        "foo": simple_configspace,
        "hello": simple_configspace,
    }
    pf = Portfolio.from_json(portfolio_json, cfg_space_map)
    assert len(pf) == 2

    cvs = list(pf)
    cvs = sorted(cvs, key=lambda cv: cv.verifier)

    assert cvs[0].verifier == "foo"
    assert cvs[1].verifier == "hello"
    assert isinstance(cvs[0].configuration, Configuration)  # TODO:
