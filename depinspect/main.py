import logging
from pathlib import Path
from shutil import rmtree
from typing import Any

import click

from depinspect.constants import (
    ARCHITECTURES,
    DATABASE_DIR,
    DB_SUFFIX,
    DISTRIBUTIONS,
    PYPROJECT_TOML,
    ROOT_DIR,
)
from depinspect.distributions import mapping
from depinspect.helper import (
    create_temp_dir,
    is_valid_architecture_name,
    is_valid_distribution_name,
    is_valid_package_name,
)

logging.basicConfig(
    level=logging.INFO,
    format="- %(levelname)s - %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def validate_distribution_name(
    ctx: click.Context,
    distribution: str,
) -> None:
    if not is_valid_distribution_name(distribution.lower()):
        raise click.BadOptionUsage(
            distribution,
            f"List of currently supported distributions: {DISTRIBUTIONS}. "
            f"Your input was: {distribution}",
        )


def validate_architecture_name(
    ctx: click.Context,
    architecture: str,
) -> None:
    if not is_valid_architecture_name(architecture.lower()):
        raise click.BadOptionUsage(
            architecture,
            f"List of currently supported architectures: {ARCHITECTURES}. "
            f"Your input was: {architecture}",
        )


def validate_package_name(
    ctx: click.Context,
    package: str,
) -> None:
    if not is_valid_package_name(package.lower()):
        raise click.BadOptionUsage(
            package,
            f"{package} is not a valid package name.",
        )


def validate_diff_args(
    ctx: click.Context,
    param: click.Parameter,
    value: tuple[tuple[str, str, str], ...],
) -> tuple[tuple[str, str, str], ...]:
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

        distribution, architecture, package_name = package_info

        validate_distribution_name(ctx, distribution)
        validate_architecture_name(ctx, architecture)
        validate_package_name(ctx, package_name)

    return value


def validate_find_divergent_args(
    ctx: click.Context,
    param: click.Parameter,
    value: tuple[tuple[str, str], ...],
) -> tuple[tuple[str, str], ...]:
    if len(value) != 2:
        raise click.BadArgumentUsage(
            "find-divergent command requires two arguments for each --arch "
            "to be provided. Incorrect number of command arguments",
            ctx=ctx,
        )

    for arch_info in value:
        if len(arch_info) != 2:
            raise click.BadArgumentUsage(
                "Distribution and architecture are required\n", ctx=ctx
            )

        distribution, architecture = arch_info
        validate_distribution_name(ctx, distribution)
        validate_architecture_name(ctx, architecture)

    return value


def validate_list_all_args(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
) -> str:
    validate_distribution_name(ctx, value)
    return value


def db_exists(db_path: Path) -> bool:
    return db_path.is_file() and db_path.suffix == ".sqlite"


@click.group()
def depinspect() -> None:
    pass


@depinspect.command(
    help=("List all available architectures and packages for a given distribution.")
)
@click.argument("distribution", callback=validate_list_all_args, nargs=1)
@click.pass_context
def list_all(ctx: click.Context, distribution: str) -> None:
    ctx.exit(0)


@depinspect.command(help=("Update metadata."))
@click.pass_context
def update(ctx: click.Context) -> None:
    config = PYPROJECT_TOML.get("tool", {}).get("depinspect", {}).get("archives", {})

    tmp_dir = create_temp_dir(dir_prefix=".tmp", output_path=ROOT_DIR)

    try:
        for distribution in DISTRIBUTIONS:
            Path.mkdir(tmp_dir / distribution)

            if not Path(DATABASE_DIR / distribution).exists():
                Path.mkdir(DATABASE_DIR / distribution)

            mapping.distribution_class_mapping[distribution].init(
                tmp_dir / distribution, config, DB_SUFFIX, DATABASE_DIR / distribution
            )
    finally:
        logging.info("Cleaning up.")
        rmtree(tmp_dir, ignore_errors=True)

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
def diff(ctx: click.Context, package: tuple[Any, ...]) -> None:
    first_argument_info, second_argument_info = package

    first_distribution, first_architecture, first_name = first_argument_info
    second_distribution, second_architecture, second_name = second_argument_info

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
        " separated by whitespace."
        " Order of arguments matters.\n\n"
        "Example: --arch ubuntu i386"
    ),
)
@click.pass_context
def find_divergent(ctx: click.Context, arch: tuple[Any, ...]) -> None:
    ctx.exit(0)
