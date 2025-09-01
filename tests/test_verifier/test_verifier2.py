import pytest
from autoverify.verifier import AbCrown, Nnenum
from autoverify.util.proc import nvidia_gpu_count


@pytest.mark.verifier
@pytest.mark.gpu
def test_allocate_run_cmd():
    verifier = Nnenum(cpu_gpu_allocation=(0, 1, -1))
    contexts = verifier.contexts or []
    run_cmd = verifier._allocate_run_cmd("foo", contexts)
    assert run_cmd == "taskset --cpu-list 0,1 foo"

    # Skip GPU allocation test if no GPUs are available
    gpus = nvidia_gpu_count()
    if gpus == 0:
        pytest.skip("No NVIDIA GPUs available")
    
    verifier = AbCrown(cpu_gpu_allocation=(0, 1, 0))
    contexts = verifier.contexts or []
    pre_len = len(contexts)
    run_cmd = verifier._allocate_run_cmd("foo", contexts)
    assert run_cmd == "taskset --cpu-list 0,1 foo"
    assert len(contexts) == pre_len + 1
