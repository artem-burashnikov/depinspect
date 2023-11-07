import tempfile
from enum import Enum
from pathlib import Path
from re import fullmatch


class Archs(Enum):
    I386 = "i386"
    ADM64 = "amd64"
    RISCV64 = "riscv64"
    ANY = "any"
    ALL = "all"


def get_project_root() -> Path:
    """
    Returns the Path object representing the root directory of the project.

    This function uses the __file__ attribute to determine the current file's path
    and then navigates up two levels to locate the project root.

    Returns:
    Path: A Path object representing the project root directory.
    """
    return Path(
        __file__
    ).parent.parent  # if helper.py is moved this breaks. Don't move!


def create_temp_dir(dir_prefix: str, output_path: Path) -> Path:
    """
    Creates a temporary directory with the given prefix in the specified output path.

    Args:
    - dir_prefix (str): The prefix for the temporary directory name.
    - output_path (Path): The Path object representing the directory where the temporary directory will be created.

    Returns:
    Path: A Path object representing the newly created temporary directory.
    """
    return Path(tempfile.mkdtemp(dir=output_path, prefix=dir_prefix))


def is_valid_package_name(package_name: str) -> bool:
    """
    Checks if a given string is a valid Unix package name.

    Args:
    - package_name (str): The name to be validated.

    Returns:
    bool: True if the package name is valid, False otherwise.

    Notes:
    - The function uses a regular expression to match the valid package name pattern.
    - A valid package name must be at least two characters, start with a letter or number, followed by letters, numbers, or the characters '+', '-', and '.'.
    """
    valid_pattern = fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9+-.]{1,})", package_name)
    return bool(valid_pattern)


def is_valid_architecture_name(architecture_name: str) -> bool:
    """
    Checks if a given string is a valid architecture name by comparing it to a predefined list of architectures.

    Args:
    - architecture_name (str): The name to be validated.

    Returns:
    bool: True if the architecture name is valid, False otherwise.

    Notes:
    - The function compares the input architecture_name with the values of a predefined enum.
    - The enum or class 'Archs' should contain valid architecture names.
    """
    return any(architecture_name == arch.value for arch in Archs)
