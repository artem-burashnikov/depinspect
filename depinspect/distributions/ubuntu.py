import logging
from pathlib import Path
from re import split

from depinspect.distributions.package import Package


class Ubuntu(Package):
    def __init__(self) -> None:
        super().__init__()
        self.distribution = "ubuntu"

    @staticmethod
    def parse_matadata(file_path: Path, dist_release: str) -> list["Package"]:
        with open(file_path) as file:
            file_content = file.read()
            ubuntu_packages: list[Package] = []

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
                            logging.warning(
                                "Ubuntu package field %s was not set. "
                                "Skipping value: %s",
                                key,
                                value,
                            )
                            pass

                    package_info.release = dist_release
                    ubuntu_packages.append(package_info)

        return ubuntu_packages

    @staticmethod
    def init(
        tmp_dir: Path,
        config: dict[str, dict[str, dict[str, dict[str, str]]]],
        distribution: str,
        db_suffix: str,
        output_path: Path,
    ) -> None:
        from depinspect.update import initialize_from_archives

        initialize_from_archives(tmp_dir, config, distribution, db_suffix, output_path)
