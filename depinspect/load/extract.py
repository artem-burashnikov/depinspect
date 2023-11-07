import logging
import lzma
from pathlib import Path

from depinspect.files import list_files_in_directory


def extract_xz_archive(archive_path: Path, output_path: Path) -> None:
    """
    Extract data from a .xz archive.

    Parameters:
    - archive_path (Path): The path to the .xz archive file.
    - output_path (Path): The path to the output file where the extracted data will be saved.

    Raises:
    - lzma.LZMAError: If there is an issue with the .xz archive.

    Returns:
    None: The function does not return a value.
    """
    with open(archive_path, "rb") as archive_file:
        with lzma.open(archive_file, "rb") as xz_file:
            extracted_data = xz_file.read()

            with open(output_path, "wb") as output_file:
                output_file.write(extracted_data)


def process_archives(archives_dir: Path) -> None:
    """
    Process archives by extracting contents and removing original archive files.

    This function takes a directory containing archives, extracts the contents of each
    archive, removes the original archive files, and returns the path to the directory
    containing the processed archives.

    Parameters:
    - archives_dir (Path): The path to the directory containing archives.

    Raises:
    - Exception: If there is an issue with extracting the archives.

    Returns:
    None: The function does not return a value.
    """
    archives_files = list_files_in_directory(archives_dir)
    try:
        for archive_path in archives_files:
            file_name = archive_path.stem
            file_extension = ".txt"
            output_path = archives_dir / f"{file_name}{file_extension}"
            extract_xz_archive(archive_path, output_path)
    except Exception:
        logging.exception(f"Failed to extract {archive_path}")
