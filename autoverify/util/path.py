"""Path/file utils."""

from pathlib import Path


def check_file_extension(file: Path, extension: str) -> bool:
    """Check if the file ends with the extension.

    Args:
        file: The file to check.
        extension: The file will be checked to end with this extension.

    Returns:
        bool: True if the file ends with the extension, False otherwise.
    """
    if not file.is_file():
        raise FileNotFoundError(f"Network {file} does not exist.")

    return file.suffix == extension


def read_path_file(file: Path) -> str:
    """Return the contents of the file the `Path` points to."""
    with open(str(file)) as f:
        s = f.read()

    return s
