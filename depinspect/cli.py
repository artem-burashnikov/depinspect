import logging
from pathlib import Path
from shutil import rmtree
from typing import Any

import click

from depinspect import printer, validator
from depinspect.constants import (
    ARCHITECTURES,
    DATABASE_DIR,
    DB_SUFFIX,
    DISTRIBUTIONS,
    PYPROJECT_TOML,
    ROOT_DIR,
)
from depinspect.distributions.mapping import distro_class_mapping
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
@click.option(
    "--distro", type=click.Choice(sorted(DISTRIBUTIONS), case_sensitive=False), nargs=1
)
@click.pass_context
def list_all(ctx: click.Context, distro: str) -> None:
    """List stored architectures and packages for a given distro.

    Provide a distribution to list all stored architectures and package names.

    Example: depinspect list-all --distro=fedora
    """

    architectures = distro_class_mapping[distro].get_all_archs()

    packages = distro_class_mapping[distro].get_stored_packages()

    printer.list_all(distro, architectures, packages)

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

            distro_class_mapping[distribution].init(
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
    "args",
    multiple=True,
    type=(str, str, str),
    callback=validator.validate_diff_args,
)
@click.pass_context
def diff(ctx: click.Context, args: tuple[Any, ...]) -> None:
    """Find a difference and similarities in dependencies of two packages.

    This command requires two sets of arguments each under -p to be specified.

    Example: depinspect diff -p ubuntu i386 apt -p ubuntu amd64 apt
    """
    arg_info_a, arg_info_b = args

    distro_a, arch_a, name_a = arg_info_a
    distro_b, arch_b, name_b = arg_info_b

    distro_class_a = distro_class_mapping[distro_a]
    depends_a = distro_class_a.get_dependencies(arch_a, name_a)

    distro_class_b = distro_class_mapping[distro_b]
    depends_b = distro_class_b.get_dependencies(arch_b, name_b)

    printer.diff(
        distro_a, arch_a, name_a, depends_a, distro_b, arch_b, name_b, depends_b
    )

    ctx.exit(0)


@depinspect.command(
    context_settings={"ignore_unknown_options": True},
    short_help=("List all packages that have divergent dependencies."),
)
@click.option(
    "--distro",
    "distro",
    type=click.Choice(sorted(DISTRIBUTIONS), case_sensitive=False),
    required=True,
)
@click.option(
    "--arch",
    "archs",
    type=click.Choice(sorted(ARCHITECTURES), case_sensitive=False),
    nargs=2,
    required=True,
)
@click.pass_context
def find_divergent(ctx: click.Context, distro: str, archs: tuple[str, str]) -> None:
    """Display all divergent packages from a given distribution and two architectures.

    This command requires distribution and two architectures to be specified.

    Example: depinspect find-divergent --distro=ubuntu --arch=riscv64 i386
    """

    distro_class = distro_class_mapping[distro]

    arch_a, arch_b = archs

    if (
        arch_a not in distro_class.get_all_archs()
        or arch_b not in distro_class.get_all_archs()
    ):
        raise click.BadArgumentUsage(
            f"Specified architectures are not present in {distro}\n", ctx=ctx
        )

    divergent = distro_class.get_divergent(arch_a, arch_b)

    printer.divergent(distro, arch_a, arch_b, divergent)

    ctx.exit(0)
