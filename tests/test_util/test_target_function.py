import pytest
from result import Ok

from autoverify.util.target_function import _process_target_function_result
from autoverify.verifier.verification_result import CompleteVerificationData, CompleteVerificationResult


def test_ok_process_tf_func_res(
    ok_complete_verif_res: CompleteVerificationResult,
):
    assert _process_target_function_result(ok_complete_verif_res, 10) == 42.0


def test_timeout_process_tf_func_res(
    timeout_complete_verif_res: CompleteVerificationResult,
):
    assert _process_target_function_result(timeout_complete_verif_res, 10) == 420.0


def test_err_process_tf_func_res(
    err_complete_verif_res: CompleteVerificationResult,
):
    with pytest.raises(Exception) as exc_info:  # noqa: B017
        _process_target_function_result(err_complete_verif_res, 10)
    # The exception should contain the CompleteVerificationData object
    assert isinstance(exc_info.value.args[0], CompleteVerificationData)


def test_err_result_process_tf_func_res(
    err_verif_res: CompleteVerificationResult,
):
    """Test that ERR results are processed correctly (no exception raised)."""
    result = _process_target_function_result(err_verif_res, 10)
    assert result == 15.0  # Should return the took time without penalty


def test_all_result_types():
    """Test that all result types are handled correctly."""
    # Test SAT result
    sat_data = CompleteVerificationData(result="SAT", took=10.0)
    sat_result = _process_target_function_result(Ok(sat_data), 2)
    assert sat_result == 10.0

    # Test UNSAT result
    unsat_data = CompleteVerificationData(result="UNSAT", took=20.0)
    unsat_result = _process_target_function_result(Ok(unsat_data), 2)
    assert unsat_result == 20.0

    # Test TIMEOUT result (should apply penalty)
    timeout_data = CompleteVerificationData(result="TIMEOUT", took=5.0)
    timeout_result = _process_target_function_result(Ok(timeout_data), 2)
    assert timeout_result == 10.0  # 5.0 * 2

    # Test ERR result (should not apply penalty)
    err_data = CompleteVerificationData(result="ERR", took=8.0)
    err_result = _process_target_function_result(Ok(err_data), 2)
    assert err_result == 8.0  # No penalty for ERR


# TODO: Tests for: get_verifier_tf, get_pick_tf, _run_verification_instance
