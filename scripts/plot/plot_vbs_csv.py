import argparse
from copy import deepcopy
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

points_template = {"x": [], "y": []}


def make_vbs_df(df: pd.DataFrame) -> pd.DataFrame:
    idx_fast = df.groupby("instance", sort=False)["took"].idxmin()
    df_vbs: pd.DataFrame = df.loc[idx_fast]

    return df_vbs


def append_points(df, points, name, n_insts):
    points[name] = deepcopy(points_template)

    n_verified = 0
    time_sum = 0

    for _, r in df.iterrows():
        time_sum += float(r["took"])  # type: ignore
        points[name]["x"].append(time_sum)

        if r["result"] == "SAT" or r["result"] == "UNSAT":
            n_verified += 1

        points[name]["y"].append(n_verified / n_insts)


def get_data_points(df: pd.DataFrame, df_vbs: pd.DataFrame, n_insts: int):
    """
    x: Cumulative time
    y: Fraction of instances verified
    """
    points = {}

    for verifier in df["verifier"].unique():
        df_v = df.loc[df["verifier"] == verifier]
        append_points(df_v, points, verifier, n_insts)

    append_points(df_vbs, points, "portfolio", n_insts)

    return points


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csv_path", type=Path, help="Path to the csv to be processed"
    )

    args = parser.parse_args()
    df = pd.read_csv(args.csv_path)
    df["instance"] = (
        df["network"] + "," + df["property"] + "," + df["timeout"].astype(str)
    )
    df = df[["verifier", "took", "instance", "result"]]

    df_vbs = make_vbs_df(df)
    data_points = get_data_points(df, df_vbs, df["instance"].nunique())

    for verifier, data in data_points.items():
        plt.plot(data["x"], data["y"], label=verifier)

    # plt.xscale("log")
    plt.xlabel("Walltime [s]")
    plt.ylabel("Frac. of instances solved")
    plt.ylim(0, 1)
    plt.legend()
    plt.show()
