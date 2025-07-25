import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from autoverify.portfolio.portfolio import (
    ConfiguredVerifier,
    Portfolio,
    PortfolioScenario,
)
from autoverify.util.resource_strategy import ResourceStrategy
from autoverify.util.verification_instance import VerificationInstance
from ConfigSpace import Configuration, ConfigurationSpace


@pytest.fixture
def portfolio_json(portfolio: Portfolio, tmp_path: Path) -> Path:
    json_path = tmp_path / "pf.json"
    portfolio.to_json(json_path)
    return json_path


@pytest.fixture
def pf_scenario_kwargs(
    trivial_instances: list[VerificationInstance], tmp_path: Path
) -> dict[str, Any]:
    return {
        "verifiers": ["nnenum", "abcrown"],
        "resources": [("nnenum", 0, 0), ("abcrown", 0, 1)],
        "instances": trivial_instances,
        "length": 4,
        "seconds_per_iter": 10.0,
        "configs_per_iter": 1,
        "alpha": 0.5,
        "added_per_iter": 1,
        "stop_early": True,
        "resource_strategy": ResourceStrategy.Auto,
        "output_dir": Path(tmp_path),
        "vnn_compat_mode": False,
        "benchmark": None,
        "verifier_kwargs": None,
        "uses_simplified_network": None,
    }


@pytest.fixture
def pf_scenario(pf_scenario_kwargs: dict[str, Any]) -> PortfolioScenario:
    pf_scen = PortfolioScenario(**pf_scenario_kwargs)

    return pf_scen


def test_faulty_pf_scenario(pf_scenario_kwargs: dict[str, Any]):
    with pytest.raises(ValueError):
        k = deepcopy(pf_scenario_kwargs)
        k["alpha"] = 300
        PortfolioScenario(**k)

    with pytest.raises(ValueError):
        k = deepcopy(pf_scenario_kwargs)
        k["vnn_compat_mode"] = True
        PortfolioScenario(**k)

    with pytest.raises(ValueError):
        k = deepcopy(pf_scenario_kwargs)
        k["verifiers"].append("verinet")
        PortfolioScenario(**k)

    with pytest.raises(ValueError):
        k = deepcopy(pf_scenario_kwargs)
        k["resources"].append(("verinet", 0, 1))
        PortfolioScenario(**k)


def test_get_smac_scen_kwargs(pf_scenario: PortfolioScenario):
    kw = pf_scenario.get_smac_scenario_kwargs()
    assert len(kw["instances"]) == 3
    assert len(kw["instance_features"]) == len(kw["instances"])
    assert kw["output_directory"].is_dir()


def test_get_smac_instances(pf_scenario: PortfolioScenario):
    insts = pf_scenario.get_smac_instances()
    assert len(insts) == len(pf_scenario.instances)


def test_get_cost(portfolio: Portfolio):
    cost = portfolio.get_cost("bar")
    assert cost == 42.0

    costs = portfolio.get_costs(["bar", "foobar"])
    assert costs == {"bar": 42.0, "foobar": 7.0}

    with pytest.raises(KeyError):
        portfolio.get_cost("hello world")


def test_to_json(portfolio: Portfolio, tmp_path: Path):
    portfolio.to_json(tmp_path / "pf.json")

    with open(tmp_path / "pf.json") as f:
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
    pf = Portfolio.from_json(Path(portfolio_json), cfg_space_map)
    assert len(pf) == 2

    cvs = list(pf)
    cvs = sorted(cvs, key=lambda cv: cv.verifier)

    assert cvs[0].verifier == "foo"
    assert cvs[1].verifier == "hello"
    assert isinstance(cvs[0].configuration, Configuration)


def test_portfolio_dunders(portfolio: Portfolio):
    cv = next(iter(portfolio))
    assert cv in portfolio

    assert len(portfolio.configs) == len(portfolio)

    with pytest.raises(ValueError):
        portfolio.add(cv)

    with pytest.raises(ValueError):
        portfolio.discard(
            ConfiguredVerifier("foooo", cv.configuration, cv.resources)
        )

    before_len = len(portfolio)
    portfolio.discard(cv)
    assert len(portfolio) == before_len - 1
    portfolio.add(cv)

    assert portfolio.str_compact().count("\n") + 1 == 2
