import argparse
from pathlib import Path

import pandas as pd


def make_vbs_df(df: pd.DataFrame) -> pd.DataFrame:
    idx_fast = df.groupby("instance")["took"].idxmin()
    df_vbs = df.loc[idx_fast]

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

    gb_verifier = df.groupby("verifier")

    h = "=" * 10 + " Stats per verifier " + "=" * 10
    print(h)

    print("Means:")
    print(gb_verifier["took"].mean())
    print()

    print("Medians:")
    print(gb_verifier["took"].median())
    print()

    print("Total times:")
    print(gb_verifier["took"].sum())
    print()

    print("Verification results:")
    res_counts = gb_verifier["result"].value_counts()
    print(res_counts)
    print()

    print("=" * len(h), "\n")

    h = "=" * 10 + " VBS Stats " + "=" * 10
    print(h)

    print("Mean:")
    print(df_vbs["took"].mean())
    print()

    print("Median:")
    print(df_vbs["took"].median())
    print()

    print("Total time:")
    print(df_vbs["took"].sum())
    print()

    print("Verification results:")
    res_counts = df_vbs["result"].value_counts()
    print(res_counts)

    print("=" * len(h), "\n")
