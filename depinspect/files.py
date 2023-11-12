import logging
from pathlib import Path


def remove_file(file_path: Path) -> None:
    """
    Remove a file at the specified path.
    """
    try:
        Path.unlink(file_path)
        logging.info(f"File '{file_path.name}' removed successfully.")
    except FileNotFoundError:
        logging.exception(f"File '{file_path.name}' was not found.")
    except PermissionError:
        logging.exception(f"Permission error: Unable to remove file '{file_path.name}")
    except OSError:
        logging.exception(f"Error removing file '{file_path.name}")


def list_files_in_directory(directory_path: Path) -> list[Path]:
    """
    List all files in the specified directory.

    Returns:
    - List[Path]: A list of Path objects representing files in the directory.
    """
    if directory_path.is_dir():
        return [path for path in Path.iterdir(directory_path) if path.is_file()]

    logging.error("list_files_in_directory: The specified path is not a directory")
    raise NotADirectoryError
