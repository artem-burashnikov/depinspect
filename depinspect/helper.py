from enum import Enum
from re import fullmatch


class Archs(Enum):
    I386 = "i386"
    ADM64 = "amd64"
    RISCV64 = "riscv64"
    ANY = "any"
    ALL = "all"


def is_valid_package_name(package_name: str) -> bool:
    """
    Check if a given string is a valid package name.

    Parameters:
    - package_name (str): The string to be checked.

    Returns:
    bool: True if the string is a valid package name, False otherwise.
    """
    valid_pattern = fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9+-.]{1,})", package_name)
    return bool(valid_pattern)


def is_valid_architecture_name(architecture_name: str) -> bool:
    """
    Check if a given string is a valid architecture name.

    Parameters:
    - architecture_name (str): The string to be checked.

    Returns:
    bool: True if the string is a valid architecture name, False otherwise.
    """
    return any(architecture_name == arch.value for arch in Archs)
