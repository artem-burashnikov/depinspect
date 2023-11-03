import lzma
from pathlib import Path

import pytest

from depinspect.load.extract import extract_xz_archive

""" 
pytest automatically recognizes tmp_path as a fixture and provides the necessary functionality
"""


def test_extract_xz_archive(tmp_path: Path) -> None:
    # Create a test .xz archive file with XZ-compressed content
    archive_path = tmp_path / "test_archive.xz"
    with open(archive_path, "wb") as archive_file:
        xz_compressed_data = lzma.compress(b"compressed_data")
        archive_file.write(xz_compressed_data)

    # Create a test output file
    output_path = tmp_path / "test_output.txt"

    # Call the function using lzma.LZMAFile for reading
    extract_xz_archive(archive_path, output_path)

    # Assert that the output file contains the expected data
    with open(output_path, "rb") as output_file:
        extracted_data = output_file.read()
        assert extracted_data == b"compressed_data"


def test_extract_xz_archive_nonexistent_archive(tmp_path: Path) -> None:
    # Test case for handling a non-existent archive file
    with pytest.raises(FileNotFoundError):
        extract_xz_archive(tmp_path / "nonexistent_archive.xz", tmp_path / "output.txt")


def test_extract_xz_archive_corrupted_archive(tmp_path: Path) -> None:
    # Create a test .xz archive file with corrupted content
    archive_path = tmp_path / "corrupted_archive.xz"
    with open(archive_path, "wb") as archive_file:
        archive_file.write(b"corrupted_data")

    # Create a test output file
    output_path = tmp_path / "corrupted_output.txt"

    # Test case for handling a corrupted archive
    with pytest.raises(lzma.LZMAError):
        extract_xz_archive(archive_path, output_path)
