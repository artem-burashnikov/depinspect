import logging
from pathlib import Path
from shutil import rmtree
from typing import Any, Tuple

import click

from depinspect import database, printer
from depinspect.constants import DB_NAME, DISTRIBUTIONS, ROOT_DIR, SOURCES_FILE_PATH
from depinspect.extract import process_archives
from depinspect.fetch import fetch_and_save_metadata
from depinspect.helper import (
    create_temp_dir,
    is_valid_architecture_name,
    is_valid_distribution,
    is_valid_package_name,
)
from depinspect.processor import run_metadata_processing

logging.basicConfig(
    level=logging.INFO,
    format="- %(levelname)s - %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def run_initialization(config_path: Path, db_name: str, output_path: Path) -> None:
    tmp_dir = create_temp_dir(dir_prefix=".tmp", output_path=output_path)
    db_path = database.new(db_name=db_name, output_path=output_path)

    try:
        logging.info("Fetching archives from pre-defined URL sources.")
        fetch_and_save_metadata(config_path, tmp_dir)

        logging.info("Extracting archives.")
        process_archives(tmp_dir)

        logging.info("Processing metadata into database.")
        for distribution in DISTRIBUTIONS:
            run_metadata_processing(tmp_dir, db_path, distribution)

    except Exception:
        logging.exception("There was an exception trying to pull data into database.")
        if db_path.is_file():
            logging.error("Removing database, if exists, as it might be corrupted.")
            database.remove(db_path)

    finally:
        logging.info("Cleaning up.")
        rmtree(tmp_dir)
        logging.info("Done.")


def validate_diff_args(
    ctx: click.Context,
    param: click.Parameter,
    value: Tuple[Tuple[str, str, str], ...],
) -> Tuple[Tuple[str, str, str], ...]:
    if len(value) != 2:
        raise click.BadArgumentUsage(
            "diff command requires two packages to be provided\n"
            "Incorrect number of command arguments",
            ctx=ctx,
        )

    for package_info in value:
        if len(package_info) != 3:
            raise click.BadArgumentUsage(
                "Distribution, architecture and name are required\n", ctx=ctx
            )
        else:
            distribution, architecture, package_name = package_info

            if not is_valid_distribution(distribution.lower()):
                raise click.BadOptionUsage(
                    distribution,
                    f"List of currently supported distributions: {DISTRIBUTIONS}. "
                    f"Your input was: {distribution}",
                )

            if not is_valid_architecture_name(architecture.lower()):
                raise click.BadOptionUsage(
                    architecture,
                    f"Archicetrure should be one of the strings provided by a "
                    f"'$ dpkg-architecture -L' command. Your input: {architecture}",
                )

            if not is_valid_package_name(package_name.lower()):
                raise click.BadOptionUsage(
                    package_name,
                    f"Name of the package should match correct syntax. "
                    f"Your input: {package_name}",
                )

    return value


def validate_find_divergent_args(
    ctx: click.Context,
    param: click.Parameter,
    value: Tuple[Tuple[str, str], ...],
) -> Tuple[Tuple[str, str], ...]:
    if len(value) != 2:
        raise click.BadArgumentUsage(
            "find-divergent command requires two architectures to be provided\n"
            "Incorrect number of command arguments",
            ctx=ctx,
        )

    for arch_info in value:
        if len(arch_info) != 2:
            raise click.BadArgumentUsage(
                "Distribution and architecture are required\n", ctx=ctx
            )
        else:
            distribution, architecture = arch_info

            if not is_valid_distribution(distribution.lower()):
                raise click.BadOptionUsage(
                    distribution,
                    f"List of currently supported distributions: {DISTRIBUTIONS}. "
                    f"Your input was: {distribution}",
                )

            if not is_valid_architecture_name(architecture.lower()):
                raise click.BadOptionUsage(
                    architecture,
                    f"Archicetrure should be one of the strings provided by a "
                    f"'$ dpkg-architecture -L' command. Your input: {architecture}",
                )

    return value


def ensure_db_exists(db_path: Path) -> None:
    if db_path.is_file() and db_path.suffix == ".db":
        return
    else:
        run_initialization(
            config_path=SOURCES_FILE_PATH, db_name=DB_NAME, output_path=ROOT_DIR
        )


@click.group()
def depinspect() -> None:
    pass


@depinspect.command(
    help=(
        "List all available distributions, architectures and packages."
        "This implicitly initializez a new database."
    )
)
@click.pass_context
def list(ctx: click.Context) -> None:
    db_path = ROOT_DIR / DB_NAME

    ensure_db_exists(db_path)

    result = database.find_all_distinct(db_path)
    printer.print_list(result)

    ctx.exit(0)


@depinspect.command(
    help=(
        "Forcefully re-initialize database. "
        "This removes old database, fetches all defined metadata "
        "and stores it in a new database."
    )
)
@click.pass_context
def update(ctx: click.Context) -> None:
    run_initialization(
        config_path=SOURCES_FILE_PATH, db_name=DB_NAME, output_path=ROOT_DIR
    )
    logging.info("Update complete.")
    ctx.exit(0)


@depinspect.command(
    help=(
        "Find a difference and similarities in dependencies of two packages "
        "from different distributions and architectures."
    ),
)
@click.option(
    "-p",
    "--package",
    multiple=True,
    type=(str, str, str),
    callback=validate_diff_args,
    help=(
        "Provide distribution, architecture and package name"
        " separated by whitespaces."
        " Order of arguments matters.\n\n"
        "Example: --package ubuntu i386 apt"
    ),
)
@click.pass_context
def diff(ctx: click.Context, package: Tuple[Any, ...]) -> None:
    db_path = ROOT_DIR / DB_NAME

    ensure_db_exists(db_path)

    result1 = database.find_dependencies(
        db_path=db_path,
        distribution=package[0][0],
        package_architecture=package[0][1],
        package_name=package[0][2],
    )

    result2 = database.find_dependencies(
        db_path=db_path,
        distribution=package[1][0],
        package_architecture=package[1][1],
        package_name=package[1][2],
    )

    printer.print_diff(package[0], result1, package[1], result2)

    ctx.exit(0)


@depinspect.command(
    help=(
        "Find all packages from specified architectures "
        "that have divergent dependencies."
    ),
)
@click.option(
    "--arch",
    multiple=True,
    type=(str, str),
    callback=validate_find_divergent_args,
    help=(
        "Provide architecture and package name"
        " separated by whitespaces."
        " Order of arguments matters.\n\n"
        "Example: --arch ubuntu i386"
    ),
)
@click.pass_context
def find_divergent(ctx: click.Context, arch: Tuple[Any, ...]) -> None:
    db_path = ROOT_DIR / DB_NAME

    ensure_db_exists(db_path)

    result1 = database.find_packages(
        db_path=db_path,
        distribution=arch[0][0],
        architecture=arch[0][1],
    )

    result2 = database.find_packages(
        db_path=db_path,
        distribution=arch[1][0],
        architecture=arch[1][1],
    )

    printer.print_divergent(arch[0], result1, arch[1], result2)

    ctx.exit(0)
