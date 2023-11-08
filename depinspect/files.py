import logging
from pathlib import Path
from typing import List


def remove_file(file_path: Path) -> None:
    try:
        Path.unlink(file_path)
        logging.info(f"File '{file_path.name}' removed successfully.")
    except FileNotFoundError:
        logging.exception(f"File '{file_path.name}' was not found.")
    except PermissionError:
        logging.exception(f"Permission error: Unable to remove file '{file_path.name}")
    except OSError:
        logging.exception(f"Error removing file '{file_path.name}")


def remove_dir(directory_path: Path) -> None:
    try:
        Path.rmdir(directory_path)
        logging.info(f"Directory '{directory_path.name}' removed successfully.")
    except NotADirectoryError:
        logging.exception(f"'{directory_path.name}' is not a directory.")
    except PermissionError:
        logging.exception(f"Unable to remove directory '{directory_path.name}'.")
    except OSError:
        logging.exception(f"Error removing directory '{directory_path.name}'.")


def list_files_in_directory(directory_path: Path) -> List[Path]:
    if directory_path.is_dir():
        files = [path for path in Path.iterdir(directory_path) if path.is_file()]
        return files
    else:
        logging.error("list_files_in_directory: The specified path is not a directory")
        raise NotADirectoryError


def list_subdirs_in_directory(directory_path: Path) -> List[Path]:
    if directory_path.is_dir():
        sub_dirs = [path for path in Path.iterdir(directory_path) if path.is_dir()]
        return sub_dirs
    else:
        logging.error(
            "list_subdirs_in_directory: The specified path is not a directory"
        )
        raise NotADirectoryError
