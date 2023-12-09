import logging
from pathlib import Path
from re import split

from depinspect.archives.extract import (
    extract_xz_archive,
    process_archives,
)
from depinspect.archives.fetch import fetch_and_save_metadata
from depinspect.database import database
from depinspect.distributions.loader import deserialize_ubuntu_metadata
from depinspect.distributions.package import Package


class Ubuntu(Package):
    def __init__(self) -> None:
        super().__init__()
        self.distribution = "ubuntu"

    @staticmethod
    def parse_metadata(file_path: Path, dist_release: str) -> list["Package"]:
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
        db_suffix: str,
        output_path: Path,
    ) -> None:
        try:
            for release in config["ubuntu"].keys():
                logging.info("Fetching archives from pre-defined URL sources.")
                fetch_and_save_metadata(config, "ubuntu", tmp_dir)

                logging.info("Extracting ubuntu xz archives.")
                process_archives(
                    input_dir=tmp_dir,
                    output_dir=tmp_dir,
                    file_extension=".txt",
                    archive_extension=".xz",
                    extractor=extract_xz_archive,
                )

                logging.info("Processing metadata into ubuntu database.")
                db_path = database.init(
                    db_name=f"ubuntu_{release}{db_suffix}", output_path=output_path
                )
                deserialize_ubuntu_metadata(tmp_dir, db_path, "ubuntu", release)
        except Exception:
            logging.exception(
                "There was an exception trying to initialize ubuntu database."
            )
