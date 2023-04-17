import sys
from pathlib import Path


def get_python_path() -> Path:
    return Path(sys.executable)
