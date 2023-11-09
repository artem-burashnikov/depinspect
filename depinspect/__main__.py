import logging
from pathlib import Path
from shutil import rmtree
from typing import Tuple

import click

from depinspect import sqlite_db
from depinspect.definitions import DB_NAME, DISTRIBUTIONS, ROOT_DIR, SOURCES_FILE_PATH
from depinspect.helper import (
    create_temp_dir,
    is_valid_architecture_name,
    is_valid_distribution,
    is_valid_package_name,
)
from depinspect.load.extract import process_archives
from depinspect.load.fetch import fetch_and_save_metadata
from depinspect.output.printer import print_result
from depinspect.process.ubuntu import run_ubuntu_metadata_processing

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="- %(levelname)s - %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-p1",
    "--package1",
    nargs=3,
    type=(str, str, str),
    help="Provide the first distribution, architecture and package name separated by whitespaces. Order of arguments matters. Example: --package1 i386 ubuntu apt",
)
@click.option(
    "-p2",
    "--package2",
    nargs=3,
    type=(str, str, str),
    help="Provide the second distribution, architecture and package name separated by whitespaces. Order of arguments matters. Example: --package2 ubuntu amd64 grub-common",
)
@click.option(
    "-l",
    "--list",
    default=False,
    is_flag=True,
    is_eager=True,
    help="List all available distributions, architectures and package names.",
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
    list: bool,
) -> None:
    """
    Main function for the depinspect command-line tool.

    Parameters:
    - ctx (click.Context): Click context object.
    - package1 (Tuple[str, str, str]): Tuple of distribution, architecture, and package name for the first package.
    - package2 (Tuple[str, str, str]): Tuple of distribution, architecture, and package name for the second package.
    - update (bool): Flag indicating whether to forcefully re-initialize the database.
    - list (bool): Flag indicating whether to list all available distributions, architectures, and package names.

    Returns:
    - None
    """

    def initialize_data(config_path: Path, db_name: str, output_path: Path) -> None:
        """
        Initialize data by fetching archives, extracting them, and processing metadata into the database.

        Parameters:
        - config_path (Path): Path to the sources configuration file.
        - db_name (str): Name of the SQLite database.
        - output_path (Path): Output path for temporary and database files.

        Returns:
        - None
        """
        tmp_dir = create_temp_dir(dir_prefix=".tmp", output_path=output_path)
        db_path = sqlite_db.db_new(db_name=db_name, output_path=output_path)

        try:
            logging.info("Fetching archives from pre-defined URL sources.")
            fetch_and_save_metadata(config_path, tmp_dir)

            logging.info("Extracting archives.")
            process_archives(tmp_dir)

            logging.info("Processing ubuntu metadata into database.")
            run_ubuntu_metadata_processing(tmp_dir, db_path)

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
        """
        Validate command-line arguments for packages.

        Parameters:
        - cl_argument1 (Tuple[str, str, str]): Tuple of distribution, architecture, and package name for the first package.
        - cl_argument2 (Tuple[str, str, str]): Tuple of distribution, architecture, and package name for the second package.

        Returns:
        - Tuple[Tuple[str, str, str], Tuple[str, str, str]]: Validated tuples for both packages.
        """
        ditribution1, architecture1, package_name1 = cl_argument1

        if not is_valid_distribution(ditribution1.lower()):
            raise click.BadOptionUsage(
                ditribution1,
                f"List of currently supported distributions: {DISTRIBUTIONS}. Your input was: {ditribution1}",
            )

        if not is_valid_architecture_name(architecture1.lower()):
            raise click.BadOptionUsage(
                architecture1,
                f"Archicetrure1 should be one of the strings provided by a '$ dpkg-architecture -L' command. Your input: {architecture1}",
            )

        if not is_valid_package_name(package_name1.lower()):
            raise click.BadOptionUsage(
                package_name1,
                f"Name of the package1 should match correct syntax. Your input: {package_name1}",
            )

        distribution2, architecture2, package_name2 = cl_argument2

        if not is_valid_distribution(distribution2.lower()):
            raise click.BadOptionUsage(
                distribution2,
                f"List of currently supported distributions: {DISTRIBUTIONS}. Your input was: {distribution2}",
            )

        if not is_valid_architecture_name(architecture2.lower()):
            raise click.BadOptionUsage(
                architecture2,
                f"Archicetrure2 should be one of the strings provided by a '$ dpkg-architecture -L' command. Your input: {architecture2}",
            )

        if not is_valid_package_name(package_name2.lower()):
            raise click.BadOptionUsage(
                package_name2,
                f"Name of the package2 should match correct syntax. Your input: {package_name2}",
            )

        return (
            (ditribution1.lower(), architecture1.lower(), package_name1.lower()),
            (distribution2.lower(), architecture2.lower(), package_name2.lower()),
        )

    def get_cl_arguments() -> Tuple[Tuple[str, str, str], Tuple[str, str, str]]:
        """
        Get validated command-line arguments for packages.

        Returns:
        - Tuple[Tuple[str, str, str], Tuple[str, str, str]]: Validated tuples for both packages.
        """
        return validate_cl_arguments(package1, package2)

    def ensure_db_exists(db_path: Path) -> None:
        """
        Ensure that the database file exists. If not, initialize data.

        Parameters:
        - db_path (Path): Path to the database file.

        Returns:
        - None
        """
        if db_path.is_file() and db_path.suffix == ".db":
            return
        else:
            initialize_data(
                config_path=SOURCES_FILE_PATH, db_name=DB_NAME, output_path=ROOT_DIR
            )

    if update and list:
        logging.error("--update and --list can't be passed simultaneously.")
        ctx.exit(1)

    if update:
        initialize_data(
            config_path=SOURCES_FILE_PATH, db_name=DB_NAME, output_path=ROOT_DIR
        )
        logging.info("Update complete.")
        ctx.exit(0)

    db_path = ROOT_DIR / DB_NAME

    if list:
        ensure_db_exists(db_path)
        sqlite_db.db_list_all(db_path)
        ctx.exit(0)

    if package1 and package2:
        validated_input1, validated_input2 = get_cl_arguments()

        ensure_db_exists(db_path)

        result1 = sqlite_db.db_list_dependencies(
            db_path=db_path,
            distribution=validated_input1[0],
            package_architecture=validated_input1[1],
            package_name=validated_input1[2],
        )

        result2 = sqlite_db.db_list_dependencies(
            db_path=db_path,
            distribution=validated_input2[0],
            package_architecture=validated_input2[1],
            package_name=validated_input2[2],
        )

        print_result(validated_input1, result1, validated_input2, result2)

    else:
        logging.error(
            "Incorrect number of arguments. Make sure to specifiy --package1 and --package2."
        )
        click.echo(ctx.get_help())
        ctx.exit(1)

    ctx.exit(0)


if __name__ == "__main__":
    main()
