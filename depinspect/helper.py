import tempfile
from pathlib import Path
from re import fullmatch


# Important! If helper.py is moved, everything breaks. Don't move the file!
def get_project_root() -> Path:
    return Path(__file__).absolute().parent.parent.resolve()


def create_temp_dir(dir_prefix: str, output_path: Path) -> Path:
    return Path(tempfile.mkdtemp(dir=output_path, prefix=dir_prefix))


def is_valid_package_name(package_name: str) -> bool:
    valid_pattern = fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9+-.]{1,})", package_name)
    return bool(valid_pattern)


def is_valid_distribution(distribution_name: str) -> bool:
    # Importing here avoids circular dependency.
    from depinspect.definitions import DISTRIBUTIONS

    return distribution_name in DISTRIBUTIONS


def is_valid_architecture_name(architecture_name: str) -> bool:
    # Importing here avoids circular dependency.
    from depinspect.definitions import ARCHITECTURES

    return architecture_name in ARCHITECTURES
