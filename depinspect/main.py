import logging
from pathlib import Path
from shutil import rmtree
from typing import Tuple

import click

from depinspect.definitions import DB_NAME, ROOT_DIR, SOURCES_FILE_PATH
from depinspect.helper import (
    create_temp_dir,
    is_valid_architecture_name,
    is_valid_package_name,
)
from depinspect.load import sqlite_db
from depinspect.load.extract import process_archives
from depinspect.load.fetch import fetch_and_save_metadata
from depinspect.load.ubuntu.metadata import run_ubuntu_metadata_processing

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="- %(levelname)s - %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@click.command()
@click.option(
    "-p1",
    "--package1",
    nargs=2,
    type=(str, str),
    # required=True,
    help="Provide the first package name alog with an architecture separated by whitespace. Example: --package1 package1-name arch1",
)
@click.option(
    "-p2",
    "--package2",
    nargs=2,
    type=(str, str),
    # required=True,
    help="Provide the second package name alog with an architecture separated by whitespace. Example: --package2 package2-name arch2",
)
@click.option(
    "--update",
    is_flag=True,
    is_eager=True,
    help="Forcefully re-initialize database. This removes old database, fetches all defined metadata and stores it in a new database.",
)
@click.pass_context
def main(
    ctx: click.Context,
    package1: Tuple[str, str],
    package2: Tuple[str, str],
    update: bool,
) -> None:
    def init(config_path: Path, db_name: str, output_path: Path) -> None:
        tmp_dir = create_temp_dir(dir_prefix=".tmp", output_path=output_path)
        db_path = sqlite_db.db_new(db_name=db_name, output_path=output_path)

        try:
            logging.info("Fetching archives from pre-defined URL sources.")
            fetch_and_save_metadata(config_path, tmp_dir)
            logging.info("Fetching: Success.")

            logging.info("Extracting archives.")
            process_archives(tmp_dir)
            logging.info("Extracting: Sucess.")

            logging.info("Processing ubuntu metadata into database.")
            run_ubuntu_metadata_processing(tmp_dir, db_path)
            logging.info("Ubuntu processing: Success.")

        except Exception:
            logging.exception(
                "There was an exception trying to pull data into database."
            )
            logging.error("Removing database, if exists, as it might be corrupted.")
            if db_path.is_file() and db_path.suffix == ".db":
                sqlite_db.db_remove(db_path)

        finally:
            logging.info("Cleaning up.")
            rmtree(tmp_dir)
            logging.info("Done.")

    # Update flag has been passed.
    if update:
        init(config_path=SOURCES_FILE_PATH, db_name=DB_NAME, output_path=ROOT_DIR)
        logging.info("Update complete.")
        ctx.exit(0)

    if not Path.joinpath(ROOT_DIR, DB_NAME).is_file():
        init(config_path=SOURCES_FILE_PATH, db_name=DB_NAME, output_path=ROOT_DIR)
    else:
        logging.info("Using existing database")

    # At this point database MUST exist in the project root either from earlier usage or (re)-initialized.
    db_path = ROOT_DIR / DB_NAME

    if not package1 or not package2:
        print(
            "\n--package1 and --package2 are required arguments\n\n"
            + main.get_help(ctx)
        )
        ctx.exit(1)

    package1_name, architecture1 = package1[0].lower(), package1[1].lower()
    if not is_valid_package_name(package1_name):
        raise click.BadOptionUsage(
            package1_name,
            f"Name of the package1 should match correct syntax. Your input: {package1_name}",
        )

    if not is_valid_architecture_name(architecture1):
        raise click.BadOptionUsage(
            architecture1,
            f"Archicetrure1 should be one of the strings provided by a '$ dpkg-architecture -L' command. Your input: {architecture1}",
        )

    package2_name, architecture2 = package2[0].lower(), package2[1].lower()
    if not is_valid_package_name(package2_name):
        raise click.BadOptionUsage(
            package2_name,
            f"Name of the package2 should match correct syntax. Your input: {package2_name}",
        )
    if not is_valid_architecture_name(architecture2):
        raise click.BadOptionUsage(
            architecture2,
            f"Archicetrure2 should be one of the strings provided by a '$ dpkg-architecture -L' command. Your input: {architecture2}",
        )

    logging.info(f"{db_path}")
    ctx.exit(0)


if __name__ == "__main__":
    main()
