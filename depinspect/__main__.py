import logging
from pathlib import Path
from shutil import rmtree
from typing import Tuple

import click

from depinspect import sqlite_db
from depinspect.definitions import DB_NAME, ROOT_DIR, SOURCES_FILE_PATH
from depinspect.helper import (
    create_temp_dir,
    is_valid_architecture_name,
    is_valid_distribution,
    is_valid_package_name,
)
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
    nargs=3,
    type=(str, str, str),
    # required=True,
    help="Provide the first distribution, architecture and package name separated by whitespaces. Order of arguments mannters. Example: --package1 i386 ubuntu apt",
)
@click.option(
    "-p2",
    "--package2",
    nargs=3,
    type=(str, str, str),
    # required=True,
    help="Provide the second distribution, architecture and package name separated by whitespaces. Order of arguments matters. Example: --package2 ubuntu amd64 grub-common",
)
@click.option(
    "-u",
    "--update",
    default=False,
    is_flag=True,
    is_eager=True,
    help="Forcefully re-initialize database. This removes old database, fetches all defined metadata and stores it in a new database.",
)
@click.pass_context
def main(
    ctx: click.Context,
    package1: Tuple[str, str, str],
    package2: Tuple[str, str, str],
    update: bool,
) -> None:
    def initialize_data(config_path: Path, db_name: str, output_path: Path) -> None:
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

    def validate_cl_arguments(
        cl_argument1: Tuple[str, str, str], cl_argument2: Tuple[str, str, str]
    ) -> Tuple[Tuple[str, str, str], Tuple[str, str, str]]:
        if not package1 or not package2:
            print("\n--package1 and --package2 are required arguments\n\n")
            ctx.exit(1)

        ditribution1, architecture1, package_name1 = (
            cl_argument1[0].lower(),
            cl_argument1[1].lower(),
            cl_argument1[2].lower(),
        )

        if not is_valid_distribution(ditribution1):
            raise click.BadOptionUsage(
                ditribution1,
                f"List of currently supported distributions: ubuntu. Your input was: {ditribution1}",
            )

        if not is_valid_architecture_name(architecture1):
            raise click.BadOptionUsage(
                architecture1,
                f"Archicetrure1 should be one of the strings provided by a '$ dpkg-architecture -L' command. Your input: {architecture1}",
            )

        if not is_valid_package_name(package_name1):
            raise click.BadOptionUsage(
                package_name1,
                f"Name of the package1 should match correct syntax. Your input: {package_name1}",
            )

        distribution2, architecture2, package_name2 = (
            cl_argument2[0].lower(),
            cl_argument2[1].lower(),
            cl_argument2[2].lower(),
        )

        if not is_valid_distribution(distribution2):
            raise click.BadOptionUsage(
                distribution2,
                f"List of currently supported distributions: ubuntu. Your input was: {distribution2}",
            )

        if not is_valid_architecture_name(architecture2):
            raise click.BadOptionUsage(
                architecture2,
                f"Archicetrure2 should be one of the strings provided by a '$ dpkg-architecture -L' command. Your input: {architecture2}",
            )

        if not is_valid_package_name(package_name2):
            raise click.BadOptionUsage(
                package_name2,
                f"Name of the package2 should match correct syntax. Your input: {package_name2}",
            )

        return (
            (ditribution1, architecture1, package_name1),
            (distribution2, architecture2, package_name2),
        )

    def get_cl_arguments() -> Tuple[Tuple[str, str, str], Tuple[str, str, str]]:
        return validate_cl_arguments(package1, package2)

    if update:
        initialize_data(
            config_path=SOURCES_FILE_PATH, db_name=DB_NAME, output_path=ROOT_DIR
        )
        logging.info("Update complete.")
        ctx.exit(0)

    # Process user input
    validated_input1, validated_input2 = get_cl_arguments()

    # If the database doesn't exist, forcefully create one and fill it with metadata.
    if not Path.joinpath(ROOT_DIR, DB_NAME).is_file():
        initialize_data(
            config_path=SOURCES_FILE_PATH, db_name=DB_NAME, output_path=ROOT_DIR
        )

    # At this point database file MUST exist in the project root either from earlier usage or (re)-initialized
    # and user input should be validated.
    db_path = ROOT_DIR / DB_NAME

    sqlite_db.db_select_query(
        db_path=db_path,
        distribution=validated_input1[0],
        package_architecture=validated_input1[1],
        package_name=validated_input1[2],
    )

    sqlite_db.db_select_query(
        db_path=db_path,
        distribution=validated_input2[0],
        package_architecture=validated_input2[1],
        package_name=validated_input2[2],
    )

    ctx.exit(0)


if __name__ == "__main__":
    main()
