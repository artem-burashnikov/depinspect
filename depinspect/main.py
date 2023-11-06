import logging
from pathlib import Path
from typing import Tuple

import click

from depinspect.helper import is_valid_architecture_name, is_valid_package_name
from depinspect.load import sqlite_db
from depinspect.load.extract import process_archives
from depinspect.load.fetch import fetch_and_save_metadata_to_tmp
from depinspect.load.ubuntu.metadata import run_ubuntu_metadata_processing

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="- %(levelname)s - %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@click.command()
@click.option(
    "--package1",
    nargs=2,
    type=(str, str),
    required=True,
    help="Provide the first package name alog with an architecture separated by whitespace. Example: --package1 package1_name arch_1",
)
@click.option(
    "--package2",
    nargs=2,
    type=(str, str),
    required=True,
    help="Provide the second package name alog with an architecture separated by whitespace. Example: --package2 package2_name arch_2",
)
def main(package1: Tuple[str, str], package2: Tuple[str, str]) -> None:
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

    logging.info(f"package1: {package1_name}, arch1: {architecture1}")
    logging.info(f"package2: {package2_name}, arch2: {architecture2}")

    tmp_dir = fetch_and_save_metadata_to_tmp()

    extracted_files_directory = process_archives(tmp_dir)

    project_root = Path.cwd()

    db_path = sqlite_db.db_new("dependencies.db", project_root)

    run_ubuntu_metadata_processing(extracted_files_directory, db_path)


if __name__ == "__main__":
    main()
