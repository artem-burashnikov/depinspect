import logging
from typing import Tuple

import click

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
    package2_name, architecture2 = package2[0].lower(), package2[1].lower()
    logging.info(f"package1: {package1_name}, arch1: {architecture1}")
    logging.info(f"package2: {package2_name}, arch2: {architecture2}")


if __name__ == "__main__":
    main()
