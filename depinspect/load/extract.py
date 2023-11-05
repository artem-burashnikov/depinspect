import lzma
import sys
from pathlib import Path
from shutil import rmtree

from depinspect.load import fetch, files


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
    archives = files.list_files_in_directory(archives_dir)
    try:
        for archive_path in archives:
            # Construct output file path
            # archive_path.parts[-1] returns for example amd64_pacakges.xz
            file_name = archive_path.parts[-1].split(".")[0]
            file_extension = ".txt"
            output_path = archives_dir / f"{file_name}{file_extension}"

            extract_xz_archive(archive_path, output_path)
            files.remove_file(archive_path)
    except Exception as e:
        print(f"Failed to extract {archive_path}\n{e}")
        print("Removing downloaded files and temprorary ditectory")
        try:
            rmtree(archives_dir)
            print(
                f"Temporary directory {archives_dir} and containing files were removed successfully"
            )
        except Exception as e:
            print(
                f"There was an error trying to clean up temproraty directory {archives_dir}\nSome files may be left and will have to be removed manually."
            )

        sys.exit(1)

    return archives_dir


if __name__ == "__main__":
    main()
