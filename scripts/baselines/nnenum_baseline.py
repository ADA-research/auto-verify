from pathlib import Path

from autoverify.portfolio.run.sequential_runner import run_sequential_portfolio
from autoverify.util.instances import read_vnncomp_instances
from autoverify.verifier import AbCrown, Nnenum

mnist_instances = read_vnncomp_instances("mnist_fc")

portfolio = [
    (Nnenum, None),  # nnenum + default config
]

results = run_sequential_portfolio(
    portfolio,  # type: ignore
    mnist_instances[:10],
    output_csv_path=Path("out.csv"),
)
