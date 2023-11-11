from abc import ABC, abstractmethod
from pathlib import Path
from re import split
from typing import List


class Package(ABC):
    def __init__(self) -> None:
        self._distribution: str = ""
        self._architecture: str = ""
        self._package: str = ""
        self._version: str = ""
        self._depends: List[str] = []
        self._recommends: List[str] = []
        self._suggests: List[str] = []
        self._enhances: List[str] = []
        self._breaks: List[str] = []
        self._conflicts: List[str] = []
        self._pre_depends: List[str] = []
        self._provides: List[str] = []

    def _str_to_list(self, string: str) -> List[str]:
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
    def depends(self) -> List[str]:
        return self._depends

    @depends.setter
    def depends(self, value: str) -> None:
        self._depends = self._str_to_list(value)

    @property
    def recommends(self) -> List[str]:
        return self._recommends

    @recommends.setter
    def recommends(self, value: str) -> None:
        self._recommends = self._str_to_list(value)

    @property
    def suggests(self) -> List[str]:
        return self._suggests

    @suggests.setter
    def suggests(self, value: str) -> None:
        self._suggests = self._str_to_list(value)

    @property
    def enhances(self) -> List[str]:
        return self._enhances

    @enhances.setter
    def enhances(self, value: str) -> None:
        self._enhances = self._str_to_list(value)

    @property
    def breaks(self) -> List[str]:
        return self._breaks

    @breaks.setter
    def breaks(self, value: str) -> None:
        self._breaks = self._str_to_list(value)

    @property
    def conflicts(self) -> List[str]:
        return self._conflicts

    @conflicts.setter
    def conflicts(self, value: str) -> None:
        self._conflicts = self._str_to_list(value)

    @property
    def pre_depends(self) -> List[str]:
        return self._pre_depends

    @pre_depends.setter
    def pre_depends(self, value: str) -> None:
        self._pre_depends = self._str_to_list(value)

    @property
    def provides(self) -> List[str]:
        return self._provides

    @provides.setter
    def provides(self, value: str) -> None:
        self._provides = self._str_to_list(value)

    @staticmethod
    @abstractmethod
    def parse_matadata(file_path: Path) -> List["Package"]:
        pass


class Ubuntu(Package):
    def __init__(self) -> None:
        super().__init__()
        self.distribution = "ubuntu"

    @staticmethod
    def parse_matadata(file_path: Path) -> List["Package"]:
        with open(file_path, "r") as file:
            file_content = file.read()
            ubuntu_packages: List[Package] = []

            blocks = split(r"\n(?=Package:)", file_content)
            for block in blocks:
                if block.strip():
                    lines = block.strip().split("\n")
                    package_info = Ubuntu()

                    for line in lines:
                        key, value = split(r":\s*", line, 1)
                        try:
                            setattr(package_info, key.lower().replace("-", "_"), value)
                        except AttributeError:
                            pass

                    ubuntu_packages.append(package_info)

        return ubuntu_packages


distribution_class_mapping = {
    "ubuntu": Ubuntu,
}
