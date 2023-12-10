import logging
from pathlib import Path

from depinspect.archives.extract import (
    extract_bz2_archive,
    extract_xz_archive,
    process_archives,
)
from depinspect.archives.fetch import fetch_and_save_metadata
from depinspect.constants import DATABASE_DIR, FEDORA_ARCHS
from depinspect.database import database
from depinspect.distributions.package import Package
from depinspect.files import list_files_in_directory


class Fedora(Package):
    @staticmethod
    def parse_metadata(file_path: Path, release: str) -> list["Package"]:
        return super(Fedora, Fedora).parse_metadata(file_path, release)

    @staticmethod
    def init(
        tmp_dir: Path,
        config: dict[str, dict[str, dict[str, dict[str, str]]]],
        db_suffix: str,
        output_path: Path,
    ) -> None:
        """
        Initialize and fetch metadata for Fedora releases.

        Parameters
        ----------
        tmp_dir : Path
            Temporary directory for fetching and extracting archives.
        config : dict[str, dict[str, dict[str, dict[str, str]]]]
            Configuration dictionary.
        db_suffix : str
            Desired file extension for the extracted databases.
        output_path : Path
            The directory where the extracted databases will be saved.
        """
        try:
            for release in config["fedora"].keys():
                logging.info("Fetching fedora archives.")
                fetch_and_save_metadata(config, "fedora", tmp_dir)

                logging.info("Extracting fedora xz archives.")
                process_archives(
                    input_dir=tmp_dir,
                    output_dir=output_path,
                    file_extension=db_suffix,
                    archive_extension=".xz",
                    extractor=extract_xz_archive,
                )

                logging.info("Extracting fedora bz2 archives.")
                process_archives(
                    input_dir=tmp_dir,
                    output_dir=output_path,
                    file_extension=db_suffix,
                    archive_extension=".bz2",
                    extractor=extract_bz2_archive,
                )
        except Exception:
            logging.exception("There was an exception trying to pull fedora database.")

    @staticmethod
    def get_all_archs() -> list[str]:
        return FEDORA_ARCHS

    @staticmethod
    def get_stored_packages() -> set[str]:
        databases = list_files_in_directory(DATABASE_DIR / "fedora")

        result: set[str] = set()

        for db_path in databases:
            result.update(database.find_all_distinct(db_path))

        return result
