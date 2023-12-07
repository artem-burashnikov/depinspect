import logging
from pathlib import Path
from shutil import rmtree

from depinspect import database
from depinspect.archives.extract import process_archives
from depinspect.archives.fetch import fetch_and_save_metadata
from depinspect.distributions.loader import deserialize_metadata
from depinspect.helper import create_temp_dir


def initialize_from_archives(
    config: dict[str, dict[str, dict[str, dict[str, str]]]],
    db_suffix: str,
    output_path: Path,
) -> None:
    tmp_dir = create_temp_dir(dir_prefix=".tmp", output_path=output_path)

    try:
        for distribution in config.keys():
            logging.info("Fetching archives from pre-defined URL sources.")
            fetch_and_save_metadata(config, tmp_dir)

            logging.info("Extracting archives.")
            process_archives(tmp_dir)

            logging.info(f"Processing metadata into {distribution} database.")
            db_path = database.init(
                db_name=f"{distribution}{db_suffix}", output_path=output_path
            )
            deserialize_metadata(tmp_dir, db_path, distribution)
    except Exception:
        logging.exception("There was an exception trying to initialize database.")
    finally:
        logging.info("Cleaning up.")
        rmtree(tmp_dir, ignore_errors=True)
