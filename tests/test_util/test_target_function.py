import pytest
from autoverify.util.target_function import _process_target_function_result
from autoverify.verifier.verification_result import CompleteVerificationResult


def test_ok_process_tf_func_res(
    ok_complete_verif_res: CompleteVerificationResult,
):
    assert _process_target_function_result(ok_complete_verif_res, 10) == 42.0


def test_timeout_process_tf_func_res(
    timeout_complete_verif_res: CompleteVerificationResult,
):
    assert (
        _process_target_function_result(timeout_complete_verif_res, 10) == 420.0
    )


def test_err_process_tf_func_res(
    err_complete_verif_res: CompleteVerificationResult,
):
    with pytest.raises(ValueError):
        _process_target_function_result(err_complete_verif_res, 10)


# TODO: Tests for: get_verifier_tf, get_pick_tf, _run_verification_instance
