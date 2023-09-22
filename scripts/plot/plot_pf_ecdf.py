import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def transform_df(df: pd.DataFrame) -> pd.DataFrame:
    df["instance"] = (
        df["network"] + "," + df["property"] + "," + df["timeout"].astype(str)
    )
    df = df[["verifier", "took", "instance", "result", "timeout"]]
    err_mask = df["result"] == "ERR"
    df.loc[err_mask, "took"] = df.loc[err_mask, "timeout"]

    return df


def setup_pf_df(df: pd.DataFrame) -> pd.DataFrame:
    result_df = df.loc[df.groupby("instance", sort=True)["took"].idxmin()]
    return result_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline_paths",
        nargs="+",
        type=Path,
        help="Path to the baselines",
        required=True,
    )
    parser.add_argument(
        "--portfolio_path",
        type=Path,
        help="Path to the portfolio",
        required=True,
    )

    args = parser.parse_args()

    baseline_dfs = []
    legend_names = []

    for baseline in args.baseline_paths:
        df = pd.read_csv(baseline)
        df = transform_df(df)
        df = df.sort_values("instance")
        baseline_dfs.append(df)
        legend_names.append(baseline.stem.split("_")[-1])
        sns.ecdfplot(df["took"], log_scale=True)

    pf_df = pd.read_csv(args.portfolio_path)
    pf_df = transform_df(pf_df)
    pf_df = setup_pf_df(pf_df)
    indices = pf_df.groupby("instance", sort=True)["took"].idxmin()
    pf_df = pf_df.loc[indices]
    pd_df = pf_df.sort_values("instance")

    sns.ecdfplot(pf_df["took"], log_scale=True)
    legend_names.append("portfolio")

    plt.xlabel("Walltime [s]")
    plt.ylabel("Fraction of instances solved")
    plt.legend(legend_names)
    plt.show()
