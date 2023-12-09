import bz2
import logging
import lzma
from collections.abc import Callable
from pathlib import Path

from depinspect.files import list_files_in_directory, remove_file


def extract_xz_archive(archive_path: Path, output_path: Path) -> None:
    with open(archive_path, "rb") as archive:
        with lzma.open(archive, "rb") as xz_archive:
            data = xz_archive.read()

            with open(output_path, "wb") as output_file:
                output_file.write(data)


def extract_bz2_archive(archive_path: Path, output_path: Path) -> None:
    with open(archive_path, "rb") as archive:
        with bz2.open(archive, "rb") as bz_archive:
            data = bz_archive.read()

            with open(output_path, "wb") as output_file:
                output_file.write(data)


def process_archives(
    input_dir: Path,
    output_dir: Path,
    file_extension: str,
    archive_extension: str,
    extractor: Callable[[Path, Path], None],
) -> None:
    archives_files = [
        file
        for file in list_files_in_directory(input_dir)
        if file.suffix == archive_extension
    ]
    try:
        for archive_path in archives_files:
            file_name = archive_path.stem
            out_file_path = output_dir / f"{file_name}{file_extension}"

            if (
                out_file_path.exists()
                and out_file_path.is_file()
                and out_file_path.suffix == file_extension
            ):
                logging.info("Removing existing fedora database.")
                remove_file(out_file_path)

            extractor(archive_path, out_file_path)
    except Exception:
        logging.exception("Failed to extract %s", archive_path)
