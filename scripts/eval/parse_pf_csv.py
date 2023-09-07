import argparse
from pathlib import Path

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csv_path", type=Path, help="Path to the csv to be processed"
    )

    args = parser.parse_args()
    csv_path = args.csv_path
    df: pd.DataFrame = pd.read_csv(csv_path)

    header = f"========== Stats for {csv_path.name} ==========\n"
    print(header)

    print("Mean:", df["took"].mean())
    print("Median:", df["took"].median())
    print("Total time:", df["took"].sum())
    print()
    print("Max:", df["took"].max())
    print("Max (non-timeout):", df[df["result"] != "TIMEOUT"]["took"].max())
    print("Max (non-err):", df[df["result"] != "ERR"]["took"].max())
    print()
    print("Min:", df["took"].min())
    print("Min (non-timeout):", df[df["result"] != "TIMEOUT"]["took"].min())
    print("Min (non-err):", df[df["result"] != "ERR"]["took"].min())
    print()

    res_counts = df["result"].value_counts()
    print("N instances:", len(df.index))
    print("SAT:", res_counts.get("SAT", 0))
    print("UNSAT:", res_counts.get("UNSAT", 0))
    print("TIMEOUT:", res_counts.get("TIMEOUT", 0))
    print("ERR:", res_counts.get("ERR", 0))
    print()

    print("=" * len(header))

    for _, row in df.iterrows():
        net = Path(row["network"]).name  # type: ignore
        prop = Path(row["property"]).name  # type: ignore
        to = row["timeout"]

        print(
            f"[[{net} :: {prop} :: {to}]] "
            f"by {row['verifier']} in {row['took']:.2f} "
            f"result = {row['result']}"
        )
