import logging
import lzma
from pathlib import Path

from depinspect.files import list_files_in_directory


def extract_xz_archive(archive_path: Path, output_path: Path) -> None:
    with open(archive_path, "rb") as archive:
        with lzma.open(archive, "rb") as xz_archive:
            extracted_data = xz_archive.read()

            with open(output_path, "wb") as output_file:
                output_file.write(extracted_data)


def process_archives(directory_path: Path) -> None:
    archives_files = list_files_in_directory(directory_path)
    try:
        for archive_path in archives_files:
            file_name = archive_path.stem
            file_extension = ".txt"
            output_path = directory_path / f"{file_name}{file_extension}"
            extract_xz_archive(archive_path, output_path)
    except Exception:
        logging.exception(f"Failed to extract {archive_path}")
