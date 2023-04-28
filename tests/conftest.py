def pytest_configure(config):
    config.addinivalue_line(
        "markers", "cpu_prop: mark test as cpu nn prop tests"
    )

    config.addinivalue_line(
        "markers", "gpu_prop: mark test as gpu nn prop tests"
    )
