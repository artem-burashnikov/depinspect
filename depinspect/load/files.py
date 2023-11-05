from pathlib import Path
from typing import List


def remove_file(file_path: Path) -> None:
    """
    Delete a file.

    Parameters:
    - file_path (Path): The path to the file to be deleted.

    Raises:
    - FileNotFoundError: If the file does not exist.
    - PermissionError: If there is a permission issue deleting the file.
    - OSError: If there is another issue with removing the file.

    Returns:
    None: The function does not return a value.
    """
    try:
        Path.unlink(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except NotADirectoryError as e:
        print(f"Directory '{file_path}' not found\n{e}")
    except PermissionError as e:
        print(f"Permission error: Unable to delete directory '{file_path}'\n{e}")
    except OSError as e:
        print(f"Error removing directory '{file_path}'\n{e}")


def remove_dir(directory_path: Path) -> None:
    """
    Remove a directory.

    Parameters:
    - directory_path (Path): The path to the directory to be removed.

    Raises:
    - NotADirectoryError: If the specified path does not point to a directory.
    - PermissionError: If there is a permission issue deleting the directory.
    - OSError: If there is another issue with removing the directory.

    Returns:
    None: The function does not return a value.
    """
    try:
        Path.rmdir(directory_path)
        print(f"Directory '{directory_path}' deleted successfully.")
    except NotADirectoryError:
        print(f"File '{directory_path}' not found.")
    except PermissionError:
        print(f"Permission error: Unable to delete file '{directory_path}'.")
    except OSError as e:
        print(f"Error removing directory '{directory_path}': {e}")


def list_files_in_directory(directory_path: Path) -> List[Path]:
    """
    List all files in a directory skipping sub-directories.

    Parameters:
    - directory_path (Path): The path to the directory.

    Raises:
    - FileNotFoundError: If the specified directory does not exist.

    Returns:
    List[Path]: A list of Path objects representing the files in the directory.
    """
    if directory_path.is_dir():
        files = [path for path in Path.iterdir(directory_path) if path.is_file()]
        return files
    else:
        raise NotADirectoryError


def list_subdirs_in_directory(directory_path: Path) -> List[Path]:
    """
    List all sub-directories in a directory skipping files.

    Parameters:
    - directory_path (Path): The path to the directory.

    Raises:
    - FileNotFoundError: If the specified parent directory does not exist.

    Returns:
    List[Path]: A list of Path objects representing the sub-directories in the directory.
    """
    if directory_path.is_dir():
        sub_dirs = [path for path in Path.iterdir(directory_path) if path.is_dir()]
        return sub_dirs
    else:
        raise NotADirectoryError
