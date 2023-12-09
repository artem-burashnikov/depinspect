import logging
from pathlib import Path


def remove_file(file_path: Path) -> None:
    try:
        Path.unlink(file_path)
        logging.info("File '%s' removed successfully.", file_path.name)
    except FileNotFoundError:
        logging.exception("File '%s' was not found.", {file_path.name})
    except PermissionError:
        logging.exception(
            "Permission error: Unable to remove file '%s'", {file_path.name}
        )
    except OSError:
        logging.exception("Error removing file '%s'", {file_path.name})


def list_files_in_directory(directory_path: Path) -> list[Path]:
    if directory_path.is_dir():
        return [path for path in Path.iterdir(directory_path) if path.is_file()]

    logging.error("list_files_in_directory: The specified path is not a directory")
    raise NotADirectoryError
