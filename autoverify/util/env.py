"""Environment util functions."""
import os
from contextlib import contextmanager


@contextmanager
def environment(**env: str):
    """Temporarily set env vars and restore values aferwards."""
    original_env = {key: os.getenv(key) for key in env}
    os.environ.update(env)

    try:
        yield
    finally:
        for key, value in original_env.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value
