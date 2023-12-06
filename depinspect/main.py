import logging
from pathlib import Path
from typing import Any

import click

from depinspect.constants import (
    ARCHITECTURES,
    DISTRIBUTIONS,
)
from depinspect.helper import (
    is_valid_architecture,
    is_valid_distribution,
    is_valid_package,
)

logging.basicConfig(
    level=logging.INFO,
    format="- %(levelname)s - %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def validate_distribution(
    ctx: click.Context,
    distribution: str,
) -> None:
    if not is_valid_distribution(distribution.lower()):
        raise click.BadOptionUsage(
            distribution,
            f"List of currently supported distributions: {DISTRIBUTIONS}. "
            f"Your input was: {distribution}",
        )


def validate_architecture(
    ctx: click.Context,
    architecture: str,
) -> None:
    if not is_valid_architecture(architecture.lower()):
        raise click.BadOptionUsage(
            architecture,
            f"List of currently supported architectures: {ARCHITECTURES}. "
            f"Your input was: {architecture}",
        )


def validate_package(
    ctx: click.Context,
    package: str,
) -> None:
    if not is_valid_package(package.lower()):
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

        validate_distribution(ctx, distribution)
        validate_architecture(ctx, architecture)
        validate_package(ctx, package_name)

    return value


def validate_find_divergent_args(
    ctx: click.Context,
    param: click.Parameter,
    value: tuple[tuple[str, str], ...],
) -> tuple[tuple[str, str], ...]:
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

        distribution, architecture = arch_info
        validate_distribution(ctx, distribution)
        validate_architecture(ctx, architecture)

    return value


def validate_list_all_args(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
) -> str:
    validate_distribution(ctx, value)
    return value


def db_exists(db_path: Path) -> bool:
    return db_path.is_file() and db_path.suffix == ".db"


@click.group()
def depinspect() -> None:
    pass


@depinspect.command(
    help=(
        "List all available architectures and packages for a given distribution."
        "This implicitly initializez a new database."
    )
)
@click.argument("distribution", callback=validate_list_all_args, nargs=1)
@click.pass_context
def list_all(ctx: click.Context, distribution: str) -> None:
    ctx.exit(0)


@depinspect.command(help=("Forcefully re-initialize databases."))
@click.pass_context
def update(ctx: click.Context) -> None:
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
