from pathlib import Path
from re import fullmatch
from sqlite3 import Connection

import click

from depinspect.constants import DISTRIBUTIONS
from depinspect.distributions.mapping import distro_class_mapping


def is_valid_package_name(pkg: str) -> bool:
    valid_pattern = fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9+-.]{1,})", pkg)
    return bool(valid_pattern)


def is_valid_distribution_name(distro: str) -> bool:
    return distro in DISTRIBUTIONS


def validate_distribution_name(
    ctx: click.Context,
    distro: str,
) -> None:
    if not is_valid_distribution_name(distro.lower()):
        raise click.BadOptionUsage(
            distro,
            f"List of currently supported distributions: {DISTRIBUTIONS}. "
            f"Your input was: {distro}",
        )


def validate_architecture_name(
    ctx: click.Context,
    distro: str,
    arch: str,
) -> None:
    archs = distro_class_mapping[distro].get_all_archs()
    if arch.lower() not in archs:
        raise click.BadOptionUsage(
            arch,
            f"List of currently supported {distro} architectures: {archs}. "
            f"Your input was: {arch}",
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
        validate_architecture_name(ctx, distribution, architecture)
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

        distro, arch = arch_info
        validate_distribution_name(ctx, distro)
        validate_architecture_name(ctx, distro, arch)

    return value


def validate_list_all_args(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
) -> str:
    validate_distribution_name(ctx, value)
    return value


def is_valid_sql_table(db: Connection, table: str) -> bool:
    res = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    tables = [elem["name"] for elem in res]
    return table in tables


def db_exists(db_path: Path) -> bool:
    return db_path.is_file() and db_path.suffix == ".sqlite"
