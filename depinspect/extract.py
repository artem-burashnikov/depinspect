import logging
import lzma
from pathlib import Path

from depinspect.files import list_files_in_directory


def extract_xz_archive(archive_path: Path, output_path: Path) -> None:
    """
    Extract data from an XZ compressed archive.

    Parameters:
    - archive_path (Path): Path to the XZ compressed archive file.
    - output_path (Path): Path to the output file where the extracted data will be saved.

    Returns:
    - None

    Note:
    This function reads the content of an XZ compressed archive file and extracts its data.
    It then writes the extracted data to the specified output file.
    """
    with open(archive_path, "rb") as archive_file:
        with lzma.open(archive_file, "rb") as xz_file:
            extracted_data = xz_file.read()

            with open(output_path, "wb") as output_file:
                output_file.write(extracted_data)


def process_archives(archives_dir: Path) -> None:
    """
    Process XZ compressed archive files in a directory.

    Parameters:
    - archives_dir (Path): Path to the directory containing XZ compressed archive files.

    Returns:
    - None

    Note:
    This function iterates through XZ compressed archive files in the specified directory,
    extracts their data using `extract_xz_archive`, and saves the extracted data as text files.
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
