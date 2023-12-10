import tempfile
from pathlib import Path
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
