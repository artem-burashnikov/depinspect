import logging
from pathlib import Path


def remove_file(file_path: Path) -> None:
    """
    Remove a file at the specified path.

    Parameters:
    - file_path (Path): The path to the file to be removed.

    Returns:
    - None

    Note:
    This function attempts to unlink (delete) the file at the provided path.
    It logs information if the file is removed successfully or logs exceptions
    if the file is not found, there's a permission error, or any other OSError occurs.
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

    Parameters:
    - directory_path (Path): The path to the directory.

    Returns:
    - List[Path]: A list of Path objects representing files in the directory.

    Raises:
    - NotADirectoryError: If the specified path is not a directory.

    Note:
    This function checks if the provided path is a directory, lists all files
    within it, and returns a list of Path objects representing the files.
    """
    if directory_path.is_dir():
        return [path for path in Path.iterdir(directory_path) if path.is_file()]

    logging.error("list_files_in_directory: The specified path is not a directory")
    raise NotADirectoryError
