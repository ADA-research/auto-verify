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
    return file.is_file() and file.suffix == extension
