import logging
from pathlib import Path
from shutil import rmtree
from typing import Any

import click

from depinspect import printer, validator
from depinspect.constants import (
    DATABASE_DIR,
    DB_SUFFIX,
    DISTRIBUTIONS,
    PYPROJECT_TOML,
    ROOT_DIR,
)
from depinspect.distributions.mapping import distribution_class_mapping
from depinspect.helper import create_temp_dir

logging.basicConfig(
    level=logging.INFO,
    format="- %(levelname)s - %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@click.group()
def depinspect() -> None:
    pass


@depinspect.command(context_settings={"ignore_unknown_options": True})
@click.argument("distribution", callback=validator.validate_list_all_args, nargs=1)
@click.pass_context
def list_all(ctx: click.Context, distribution: str) -> None:
    """List stored architectures and packages for a given distro.

    Provide a distribution to list all stored architectures and package names.

    Example: depinspect list-all fedora
    """

    architectures = distribution_class_mapping[distribution].get_all_archs()

    packages = distribution_class_mapping[distribution].get_stored_packages()

    printer.list_all(distribution, architectures, packages)

    ctx.exit(0)


@depinspect.command(context_settings={"ignore_unknown_options": True})
@click.pass_context
def update(ctx: click.Context) -> None:
    """Update metadata stored in databases."""
    config = PYPROJECT_TOML.get("tool", {}).get("depinspect", {}).get("archives", {})

    tmp_dir = create_temp_dir(dir_prefix=".tmp", output_path=ROOT_DIR)

    try:
        for distribution in DISTRIBUTIONS:
            Path.mkdir(tmp_dir / distribution)

            if not Path(DATABASE_DIR / distribution).exists():
                Path.mkdir(DATABASE_DIR / distribution)

            distribution_class_mapping[distribution].init(
                tmp_dir / distribution, config, DB_SUFFIX, DATABASE_DIR / distribution
            )
    finally:
        logging.info("Cleaning up.")
        rmtree(tmp_dir, ignore_errors=True)

    ctx.exit(0)


@depinspect.command(
    context_settings={"ignore_unknown_options": True},
    short_help=("Compare two packages."),
)
@click.option(
    "-p",
    "--package",
    multiple=True,
    type=(str, str, str),
    callback=validator.validate_diff_args,
)
@click.pass_context
def diff(ctx: click.Context, package: tuple[Any, ...]) -> None:
    """Find a difference and similarities in dependencies of two packages.

    This command requires two sets of arguments each under --package to be specified.

    Example: depinspect diff -p ubuntu i386 apt -p ubuntu amd64 apt
    """
    arg_info_a, arg_info_b = package

    distro_a, arch_a, name_a = arg_info_a
    distro_b, arch_b, name_b = arg_info_b

    distro_class_a = distribution_class_mapping[distro_a]
    depends_a = distro_class_a.get_dependencies(arch_a, name_a)

    distro_class_b = distribution_class_mapping[distro_b]
    depends_b = distro_class_b.get_dependencies(arch_b, name_b)

    printer.print_diff(
        distro_a, arch_a, name_a, depends_a, distro_b, arch_b, name_b, depends_b
    )

    ctx.exit(0)


@depinspect.command(
    context_settings={"ignore_unknown_options": True},
    short_help=("List all packages that have divergent dependencies."),
)
@click.option(
    "--arch",
    multiple=True,
    type=(str, str),
    callback=validator.validate_find_divergent_args,
)
@click.pass_context
def find_divergent(ctx: click.Context, arch: tuple[Any, ...]) -> None:
    ctx.exit(0)
