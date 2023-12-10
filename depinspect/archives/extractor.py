import bz2
import logging
import lzma
from collections.abc import Callable
from pathlib import Path

from depinspect.files import list_files_in_directory, remove_file


def extract_xz_archive(archive_path: Path, output_path: Path) -> None:
    """
    Extract the contents of an XZ archive to a specified output file.

    Parameters
    ----------
    archive_path : Path
        Path to the XZ-compressed archive.
    output_path : Path
        Path to the output file where the contents will be written.
    """
    with lzma.open(archive_path, "rb") as xz_archive:
        data = xz_archive.read()

        with open(output_path, "wb") as output_file:
            output_file.write(data)


def extract_bz2_archive(archive_path: Path, output_path: Path) -> None:
    """
    Extract the contents of a BZ2 archive to a specified output file.

    Parameters
    ----------
    archive_path : Path
        Path to the BZ2-compressed archive.
    output_path : Path
        Path to the output file where the contents will be written.
    """
    with bz2.open(archive_path, "rb") as bz_archive:
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
    """
    Process archives in the input directory.

    Parameters
    ----------
    input_dir : Path
        Path to the directory containing input archives.
    output_dir : Path
        Path to the directory where extracted files will be saved.
    file_extension : str
        Desired file extension for the extracted files.
    archive_extension : str
        File extension of the archives to be processed.
    extractor : Callable[[Path, Path], None]
        Extractor function to be applied to each archive.
    """
    archives_files = [
        file
        for file in list_files_in_directory(input_dir)
        if file.suffix == archive_extension
    ]
    try:
        for archive_path in archives_files:
            file_name = archive_path.stem
            out_file_path = output_dir / f"{file_name}{file_extension}"

            # If an output file with the same name and extension exists, remove it
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
