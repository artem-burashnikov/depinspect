from abc import ABC, abstractmethod
from pathlib import Path


class Package(ABC):
    def __init__(self) -> None:
        self._distribution: str = ""
        self._architecture: str = ""
        self._package: str = ""
        self._version: str = ""
        self._depends: list[str] = []
        self._recommends: list[str] = []
        self._suggests: list[str] = []
        self._enhances: list[str] = []
        self._breaks: list[str] = []
        self._conflicts: list[str] = []
        self._pre_depends: list[str] = []
        self._provides: list[str] = []

    def _str_to_list(self, string: str) -> list[str]:
        return [string.strip() for string in string.split(",")]

    @property
    def distribution(self) -> str:
        return self._distribution

    @distribution.setter
    def distribution(self, value: str) -> None:
        self._distribution = value

    @property
    def architecture(self) -> str:
        return self._architecture

    @architecture.setter
    def architecture(self, value: str) -> None:
        self._architecture = value

    @property
    def package(self) -> str:
        return self._package

    @package.setter
    def package(self, value: str) -> None:
        self._package = value

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        self._version = value

    @property
    def depends(self) -> list[str]:
        return self._depends

    @depends.setter
    def depends(self, value: str) -> None:
        self._depends = self._str_to_list(value)

    @property
    def recommends(self) -> list[str]:
        return self._recommends

    @recommends.setter
    def recommends(self, value: str) -> None:
        self._recommends = self._str_to_list(value)

    @property
    def suggests(self) -> list[str]:
        return self._suggests

    @suggests.setter
    def suggests(self, value: str) -> None:
        self._suggests = self._str_to_list(value)

    @property
    def enhances(self) -> list[str]:
        return self._enhances

    @enhances.setter
    def enhances(self, value: str) -> None:
        self._enhances = self._str_to_list(value)

    @property
    def breaks(self) -> list[str]:
        return self._breaks

    @breaks.setter
    def breaks(self, value: str) -> None:
        self._breaks = self._str_to_list(value)

    @property
    def conflicts(self) -> list[str]:
        return self._conflicts

    @conflicts.setter
    def conflicts(self, value: str) -> None:
        self._conflicts = self._str_to_list(value)

    @property
    def pre_depends(self) -> list[str]:
        return self._pre_depends

    @pre_depends.setter
    def pre_depends(self, value: str) -> None:
        self._pre_depends = self._str_to_list(value)

    @property
    def provides(self) -> list[str]:
        return self._provides

    @provides.setter
    def provides(self, value: str) -> None:
        self._provides = self._str_to_list(value)

    @staticmethod
    @abstractmethod
    def parse_matadata(file_path: Path) -> list["Package"]:
        pass
