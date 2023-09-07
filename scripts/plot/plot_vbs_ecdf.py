import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def make_vbs_df(df: pd.DataFrame) -> pd.DataFrame:
    idx_fast = df.groupby("instance", sort=False)["took"].idxmin()
    df_vbs: pd.DataFrame = df.loc[idx_fast]

    return df_vbs


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

    sns.color_palette()
    legend_names = ["VBS PF"]

    sns.ecdfplot(df_vbs["took"], log_scale=True, palette="deep")
    for verifier in df["verifier"].unique():
        df_verifier = df[df["verifier"] == verifier]
        sns.ecdfplot(df_verifier["took"], log_scale=True, palette="deep")
        legend_names.append(verifier)

    plt.xlabel("Walltime [s]")
    plt.ylabel("Fraction of instances solved")
    plt.legend(legend_names)
    plt.show()
