from click import echo

from depinspect.constants import MAX_CHAR_LENGTH


def print_for_one(
    distro: str,
    arch: str,
    name: str,
    depends: set[str],
) -> None:
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


def print_diff(
    distro_a: str,
    arch_a: str,
    name_a: str,
    depends_a: set[str],
    distro_b: str,
    arch_b: str,
    name_b: str,
    depends_b: set[str],
) -> None:
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


def list_all(distribution: str, archs: list[str], packages: set[str]) -> None:
    echo(f"Distribution: {distribution}")

    echo(f"Architectures: {', '.join(list(archs))}")

    echo("Packages:")
    for package in sorted(packages):
        echo(package)


# def print_divergent(
#     dist_and_arch1: tuple[str, str],
#     query_result1: dict[str, list[str]],
#     dist_and_arch2: tuple[str, str],
#     query_result2: dict[str, list[str]],
# ) -> None:
#     set_of_packages1 = set(query_result1.keys())
#     set_of_packages2 = set(query_result2.keys())

#     definitely_divergent = set.symmetric_difference(set_of_packages1, set_of_packages2)
#     maybe_divergent = set_of_packages1.intersection(set_of_packages2)

#     divergent_packages: list[str] = []
#     for package_name in maybe_divergent:
#         if sorted(query_result1[package_name]) != sorted(query_result2[package_name]):
#             divergent_packages.append(package_name)

#     divergent_packages.extend(definitely_divergent)

#     echo(
#         f"# The following packages have divergent dependencies "
#         f"in {dist_and_arch1} and {dist_and_arch2}"
#     )

#     for package_name in divergent_packages:
#         echo(package_name)

#     echo("\n", nl=False)
