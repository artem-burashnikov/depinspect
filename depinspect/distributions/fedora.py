import logging
from pathlib import Path

from depinspect.archives.extract import (
    extract_bz2_archive,
    extract_xz_archive,
    process_archives,
)
from depinspect.archives.fetch import fetch_and_save_metadata
from depinspect.distributions.package import Package


class Fedora(Package):
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
