import tempfile
from pathlib import Path
from re import fullmatch
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


# Important! If helper.py is moved, everything breaks. Don't move the file!
def get_project_root() -> Path:
    """
    Get the absolute path to the root directory of the project.

    Note
    ----
    This function uses the absolute path of the current file and navigates
    two levels up to determine the project root directory.
    """
    return Path(__file__).absolute().parent.parent.resolve()


def create_temp_dir(dir_prefix: str, output_path: Path) -> Path:
    return Path(tempfile.mkdtemp(dir=output_path, prefix=dir_prefix))


def is_valid_package_name(package_name: str) -> bool:
    valid_pattern = fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9+-.]{1,})", package_name)
    return bool(valid_pattern)


def is_valid_distribution_name(distribution_name: str) -> bool:
    from depinspect.constants import DISTRIBUTIONS

    return distribution_name in DISTRIBUTIONS


def is_valid_architecture_name(architecture_name: str) -> bool:
    from depinspect.constants import ARCHITECTURES

    return architecture_name in ARCHITECTURES


def parse_pyproject(pyproject_file: Path) -> Any:
    """
    Parse the contents of a 'pyproject.toml' file.

    Parameters
    ----------
    pyproject_file : Path
        Path to the 'pyproject.toml' file to be parsed.

    Returns
    -------
    The parsed content of the 'pyproject.toml' file.
    """
    with open(pyproject_file, "rb") as file:
        return tomllib.load(file)
