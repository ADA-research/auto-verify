from autoverify.verifier import AbCrown, Nnenum


def test_allocate_run_cmd():
    verifier = Nnenum(cpu_gpu_allocation=(0, 1, -1))
    contexts = verifier.contexts or []
    run_cmd = verifier._allocate_run_cmd("foo", contexts)
    assert run_cmd == "taskset --cpu-list 0,1 foo"

    verifier = AbCrown(cpu_gpu_allocation=(0, 1, 0))
    contexts = verifier.contexts or []
    pre_len = len(contexts)
    run_cmd = verifier._allocate_run_cmd("foo", contexts)
    assert run_cmd == "taskset --cpu-list 0,1 foo"
    assert len(contexts) == pre_len + 1
