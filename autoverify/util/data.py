"""Functions for pasing verification data.

VerificationDataResult cols:

network
property
timeout
verifier
config
success
result
took
counter_example
error_string

"""
import pandas as pd


def get_mean_median(df: pd.DataFrame) -> tuple[float, float]:
    took = df.loc[:, "took"]
    return float(took.mean()), float(took.median())
