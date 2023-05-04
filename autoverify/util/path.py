from pathlib import Path


def verify_extension(file: Path, extension: str) -> bool:
    return str(file).lower().endswith(extension)
