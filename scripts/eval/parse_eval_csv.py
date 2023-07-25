import argparse

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Path to the csv to be processed")

    args = parser.parse_args()
    csv_path = args.csv_path
    print(f"====== Processing {csv_path} ======")

    df: pd.DataFrame = pd.read_csv(csv_path)
    print("Mean:", df["took"].mean())
    print("Median:", df["took"].median())
    print("Total time:", df["took"].sum())

    res_counts = df["result"].value_counts()
    print("SAT:", res_counts.get("SAT", 0))
    print("UNSAT:", res_counts.get("UNSAT", 0))
    print("TIMEOUT:", res_counts.get("TIMEOUT", 0))
    print("ERR:", res_counts.get("ERR", 0))
