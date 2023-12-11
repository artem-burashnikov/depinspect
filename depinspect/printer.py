from click import echo

from depinspect.constants import MAX_CHAR_LENGTH


def print_for_one(
    distro: str,
    arch: str,
    name: str,
    depends: set[str],
) -> None:
    """Print package information for a single package."""
    header = f"{distro} - {arch} - {name}"

    divider = "=" * MAX_CHAR_LENGTH

    echo("\n", nl=False)
    echo(header)
    echo(divider)
    for pkg in sorted(depends):
        echo(f"{pkg}")
    echo("\n", nl=False)


def print_for_both(
    distro_a: str,
    arch_a: str,
    name_a: str,
    depends_a: set[str],
    distro_b: str,
    arch_b: str,
    name_b: str,
    depends_b: set[str],
) -> None:
    """Print package comparison information for two packages."""
    title_both = "These dependencies are present in both:"
    title_exclusive = "These dependencies are exclusive to:"

    header_a = f"{distro_a} - {arch_a} - {name_a}"
    header_b = f"{distro_b} - {arch_b} - {name_b}"

    divider = "=" * MAX_CHAR_LENGTH

    intersection = sorted(depends_a.intersection(depends_b))
    a_minus_b = sorted(depends_a.difference(depends_b))
    b_minus_a = sorted(depends_b.difference(depends_a))

    echo("\n", nl=False)
    echo(title_both)
    echo(header_a)
    echo(header_b)
    echo(divider)
    for pkg in intersection:
        echo(pkg)
    echo("\n", nl=False)

    echo(title_exclusive)
    echo(header_a)
    echo(divider)
    for pkg in a_minus_b:
        echo(pkg)
    echo("\n", nl=False)

    echo(title_exclusive)
    echo(header_b)
    echo(divider)
    for pkg in b_minus_a:
        echo(f"{pkg}")
    echo("\n", nl=False)


def diff(
    distro_a: str,
    arch_a: str,
    name_a: str,
    depends_a: set[str],
    distro_b: str,
    arch_b: str,
    name_b: str,
    depends_b: set[str],
) -> None:
    """Print the difference in dependencies between two packages."""
    if not depends_a and not depends_b:
        echo(
            f"No records were found in the database for\n"
            f"{distro_a} - {arch_a} - {name_a}\n"
            f"{distro_b} - {arch_b} - {name_b}"
        )

    elif not depends_a and depends_b:
        echo(f"\nNo records found for {distro_a} - {arch_a} - {name_a}")
        print_for_one(distro_b, arch_b, name_b, depends_b)

    elif depends_a and not depends_b:
        echo(f"\nNo records found for {distro_b} - {arch_b} - {name_b}")
        print_for_one(distro_a, arch_a, name_a, depends_a)

    else:
        print_for_both(
            distro_a,
            arch_a,
            name_a,
            depends_a,
            distro_b,
            arch_b,
            name_b,
            depends_b,
        )


def list_all(distro: str, archs: set[str], pkgs: set[str]) -> None:
    """Print information about architectures, and packages.

    Parameters
    ----------
    distro : str
        The name of the Linux distribution.
    archs : set[str]
        Set of architectures available for the distribution.
    pkgs : set[str]
        Set of package names available for the distribution.

    Returns
    -------
    None
    """
    echo(f"Distribution: {distro}")

    echo(f"Architectures: {', '.join(archs)}")

    echo("Packages:")
    for pkg in sorted(pkgs):
        echo(pkg)


def divergent(distro: str, arch_a: str, arch_b: str, pkgs: set[str]) -> None:
    """Print information about packages with divergent dependencies."""
    echo(f"Distribution: {distro}")

    echo(f"Compared architectures: {arch_a} - {arch_b}")

    echo("Packages:")
    for pkg in sorted(pkgs):
        echo(pkg)
