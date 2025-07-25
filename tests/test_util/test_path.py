from pathlib import Path

import pytest
from autoverify.util.path import check_file_extension, read_path_file

SampleFiles = tuple[Path, Path]


@pytest.fixture
def sample_files(tmp_path: Path) -> SampleFiles:
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.csv"

    file1.write_text("This is file 1.")
    file2.write_text("This is file 2.")

    return file1, file2


def test_check_file_extension_with_matching_extension(
    sample_files: SampleFiles,
):
    file1, file2 = sample_files
    assert check_file_extension(file1, ".txt")
    assert check_file_extension(file2, ".csv")


def test_check_file_extension_with_non_matching_extension(
    sample_files: SampleFiles,
):
    file1, file2 = sample_files
    assert not check_file_extension(file1, ".csv")
    assert not check_file_extension(file2, ".txt")


def test_check_file_extension_with_nonexistent_file():
    file = Path("non_existent_file.txt")

    with pytest.raises(FileNotFoundError):
        check_file_extension(file, ".txt")


def test_read_path_file(sample_files: SampleFiles):
    file1, file2 = sample_files
    content1 = read_path_file(file1)
    content2 = read_path_file(file2)

    assert content1 == "This is file 1."
    assert content2 == "This is file 2."


def test_read_path_file_with_nonexistent_file():
    file = Path("non_existent_file.txt")

    with pytest.raises(FileNotFoundError):
        read_path_file(file)


def test_read_path_file_with_empty_file(tmp_path: Path):
    empty_file = tmp_path / "empty_file.txt"
    empty_file.write_text("")

    content = read_path_file(empty_file)
    assert content == ""
