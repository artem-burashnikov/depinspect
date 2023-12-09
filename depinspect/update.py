import logging
from pathlib import Path

from depinspect.archives.extract import process_archives
from depinspect.archives.fetch import fetch_and_save_metadata
from depinspect.database import database
from depinspect.distributions.loader import deserialize_metadata


def initialize_from_archives(
    tmp_dir: Path,
    config: dict[str, dict[str, dict[str, dict[str, str]]]],
    distribution: str,
    db_suffix: str,
    output_path: Path,
) -> None:
    try:
        for release in config[distribution].keys():
            logging.info("Fetching archives from pre-defined URL sources.")
            fetch_and_save_metadata(config, tmp_dir)

            logging.info("Extracting archives.")
            process_archives(tmp_dir)

            logging.info("Processing metadata into %s database.", distribution)
            db_path = database.init(
                db_name=f"{distribution}{db_suffix}", output_path=output_path
            )
            deserialize_metadata(tmp_dir, db_path, distribution, release)
    except Exception:
        logging.exception("There was an exception trying to initialize database.")
