import lzma
import sys
from pathlib import Path

from depinspect.load import fetch, file_management


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


def main() -> Path:
    """
    Process archives by extracting contents and removing original archive files.

    Returns:
    Path: The path to the directory containing processed archives.
    """
    archives_dir = fetch.main()
    archives = file_management.list_files_in_directory(archives_dir)

    for count, archive_path in enumerate(archives):
        try:
            # Construct output file path
            file_prefix = count
            file_name = "_Packages"
            file_extension = ".txt"
            output_path = archives_dir / f"{file_prefix}{file_name}{file_extension}"

            extract_xz_archive(archive_path, output_path)
        except Exception as e:
            print(f"Failed to extract {archive_path}", {e})
            sys.exit(1)
        file_management.remove_file(archive_path)

    return archives_dir


if __name__ == "__main__":
    main()
