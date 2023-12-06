import logging
import lzma
from pathlib import Path

from depinspect.files import list_files_in_directory


def extract_xz_archive(archive_path: Path, output_path: Path) -> None:
    with open(archive_path, "rb") as archive_file:
        with lzma.open(archive_file, "rb") as xz_file:
            extracted_data = xz_file.read()

            with open(output_path, "wb") as output_file:
                output_file.write(extracted_data)


def process_archives(archives_dir: Path) -> None:
    archives_files = list_files_in_directory(archives_dir)
    try:
        for archive_path in archives_files:
            file_name = archive_path.stem
            file_extension = ".txt"
            output_path = archives_dir / f"{file_name}{file_extension}"
            extract_xz_archive(archive_path, output_path)
    except Exception:
        logging.exception(f"Failed to extract {archive_path}")
