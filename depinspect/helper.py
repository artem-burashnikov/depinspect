import tempfile
from pathlib import Path
from re import fullmatch


# Important! If helper.py is moved, everything breaks. Don't move the file!
def get_project_root() -> Path:
    """
    Get the absolute path to the root directory of the project.

    Returns:
    - Path: The absolute path to the root directory of the project.

    Note:
    This function uses the absolute path of the current file and navigates
    two levels up to determine the project root directory.
    """
    return Path(__file__).absolute().parent.parent.resolve()


def create_temp_dir(dir_prefix: str, output_path: Path) -> Path:
    """
    Create a temporary directory with a specified prefix in the given output path.

    Parameters:
    - dir_prefix (str): The prefix to use for the temporary directory.
    - output_path (Path): The path where the temporary directory will be created.

    Returns:
    - Path: The path to the newly created temporary directory.
    """
    return Path(tempfile.mkdtemp(dir=output_path, prefix=dir_prefix))


def is_valid_package_name(package_name: str) -> bool:
    """
    Check if a package name is valid.

    Parameters:
    - package_name (str): The package name to be validated.

    Returns:
    - bool: True if the package name is valid, False otherwise.

    Note:
    This function uses a regular expression pattern to check if the package name
    follows the specified format: starts with an alphanumeric character, followed
    by alphanumeric characters or '+', '-', or '.' with a minimum length of 2.
    """
    valid_pattern = fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9+-.]{1,})", package_name)
    return bool(valid_pattern)


def is_valid_distribution(distribution_name: str) -> bool:
    """
    Check if a distribution name is valid.

    Parameters:
    - distribution_name (str): The distribution name to be validated.

    Returns:
    - bool: True if the distribution name is valid, False otherwise.

    Note:
    This function checks if the provided distribution name is present in a predefined
    list of valid distributions.
    """
    # Importing here avoids circular dependency.
    from depinspect.constants import DISTRIBUTIONS

    return distribution_name in DISTRIBUTIONS


def is_valid_architecture_name(architecture_name: str) -> bool:
    """
    Check if an architecture name is valid.

    Parameters:
    - architecture_name (str): The architecture name to be validated.

    Returns:
    - bool: True if the architecture name is valid, False otherwise.

    Note:
    This function checks if the provided architecture name is present in a predefined
    list of valid architectures.
    """
    # Importing here avoids circular dependency.
    from depinspect.constants import ARCHITECTURES

    return architecture_name in ARCHITECTURES
