from enum import Enum
from re import fullmatch


class Archs(Enum):
    I386 = "i386"
    ADM64 = "amd64"
    RISCV64 = "riscv64"
    ANY = "any"
    ALL = "all"


def is_valid_package_name(package_name: str) -> bool:
    valid_pattern = fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9+-.]{1,})", package_name)
    return bool(valid_pattern)


def is_valid_architecture_name(architecture_name: str) -> bool:
    return any(architecture_name == arch.value for arch in Archs)
