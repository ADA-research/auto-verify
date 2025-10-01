import pytest
from ConfigSpace import Configuration

from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio
from autoverify.portfolio.portfolio_runner import PortfolioRunner


@pytest.fixture
def faulty_pf(pf_cfg: Configuration, pf_cfg2: Configuration) -> Portfolio:
    pf = Portfolio()
    pf.add(ConfiguredVerifier("foo", pf_cfg, resources=(1, 0)))
    pf.add(ConfiguredVerifier("foo2", pf_cfg2, resources=(2000000, 1)))
    pf.add(ConfiguredVerifier("foo3", pf_cfg2, resources=(0, 1)))

    pf.update_costs({"bar": 42.0})
    pf.update_costs({"foobar": 7.0})

    return pf


def test_init_runner(portfolio: Portfolio, faulty_pf: Portfolio):
    with pytest.raises(RuntimeError):
        _ = PortfolioRunner(faulty_pf, n_cpu=16, n_gpu=1)

    runner = PortfolioRunner(portfolio, n_cpu=16, n_gpu=1)
    allocs = [(8, 15, -1), (0, 7, 0)]
    allocs2 = [(8, 15, 0), (0, 7, -1)]

    assert all(
        alloc in list(runner._allocation.values()) for alloc in allocs
    ) or all(alloc in list(runner._allocation.values()) for alloc in allocs2)
