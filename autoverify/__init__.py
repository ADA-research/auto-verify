import os
from pathlib import Path

__version__ = "0.1.0"

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_VERIFICATION_TIMEOUT_SEC = 600
