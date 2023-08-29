from autoverify.portfolio.portfolio import Portfolio
from autoverify.portfolio.portfolio_runner import PortfolioRunner


def test_init_runner(portfolio: Portfolio):
    runner = PortfolioRunner(portfolio)
    for k, v in runner._allocation.items():
        print(k, v)
    assert False
