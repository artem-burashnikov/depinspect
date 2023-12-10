from pathlib import Path
from re import fullmatch

import click

from depinspect.constants import ARCHITECTURES, DISTRIBUTIONS


def is_valid_package_name(package_name: str) -> bool:
    valid_pattern = fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9+-.]{1,})", package_name)
    return bool(valid_pattern)


def is_valid_distribution_name(distribution_name: str) -> bool:
    return distribution_name in DISTRIBUTIONS


def is_valid_architecture_name(architecture_name: str) -> bool:
    return architecture_name in ARCHITECTURES


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
