from pathlib import Path

import pandas as pd
import pytest

from autoverify.util.verification_instance import VerificationInstance
from autoverify.verifier import Nnenum
from autoverify.verify.eval_verifier import eval_verifier


@pytest.mark.verifier
def test_eval_verifier(
    nnenum: Nnenum,
    trivial_instances: list[VerificationInstance],
    tmp_path: Path,
):
    tmp_csv = tmp_path / "tmp_res.csv"
    tmp_csv.touch()

    eval_verifier(
        nnenum,
        trivial_instances,
        None,
        warmup=False,
        output_csv_path=tmp_csv,
    )

    df = pd.read_csv(tmp_csv)

    assert len(df.index) == 3

    row_sat = df.iloc[0]
    assert row_sat["network"] == "test_sat.onnx"
    assert row_sat["property"] == "test_prop.vnnlib"
    assert row_sat["timeout"] == 60
    assert row_sat["verifier"] == "nnenum"
    assert row_sat["config"] == "default"
    assert row_sat["success"] == "OK"
    assert row_sat["result"] == "SAT"
    assert float(row_sat["took"])
    assert not pd.isna(row_sat["counter_example"])
    assert pd.isna(row_sat["stderr"])
    assert not pd.isna(row_sat["stdout"])
