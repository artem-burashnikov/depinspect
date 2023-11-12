from click import echo


def print_diff(
    dist_arch_and_package_name1: tuple[str, str, str],
    query_result1: list[tuple[str]],
    dist_arch_and_package_name2: tuple[str, str, str],
    query_result2: list[tuple[str]],
) -> None:
    def print_for_one(
        dist_arch_and_package_name: tuple[str, str, str], query_result: list[tuple[str]]
    ) -> None:
        distribution, architecture, package_name = dist_arch_and_package_name
        dependencies = sorted(query_result[0][0].split(","))
        header = f"{distribution} - {architecture} - {package_name}"

        max_char_length = (
            len(max(dependencies, key=len)) if len(dependencies) != 0 else len(header)
        )

        divider = "=" * max_char_length

        echo("\n", nl=False)
        echo(header)
        echo(divider)
        for dependency in dependencies:
            echo(f"{dependency}")
        echo("\n", nl=False)

    def print_for_both(
        dist_arch_and_package_name1: tuple[str, str, str],
        query_result1: list[tuple[str]],
        dist_arch_and_package_name2: tuple[str, str, str],
        query_result2: list[tuple[str]],
    ) -> None:
        distribution1, architecture1, package_name1 = dist_arch_and_package_name1
        dependencies1 = sorted(query_result1[0][0].split(","))
        title1 = "These dependencies are present in both:"
        header1 = f"{distribution1} - {architecture1} - {package_name1}"

        distribution2, architecture2, package_name2 = dist_arch_and_package_name2
        dependencies2 = sorted(query_result2[0][0].split(","))
        title2 = "These dependencies are exclusive to:"
        header2 = f"{distribution2} - {architecture2} - {package_name2}"

        matches = sorted(set(dependencies1).intersection(dependencies2))
        exclusive_to_first = sorted(set(dependencies1).difference(set(dependencies2)))
        exclusive_to_second = sorted(set(dependencies2).difference(set(dependencies1)))

        max_header_length = len(max(header1, header2, key=len))

        match_max_length = max(
            len(max(matches, key=len, default="")), max_header_length
        )

        diff_max_length1 = max(
            len(max(exclusive_to_first, key=len, default="")), max_header_length
        )

        diff_max_length2 = max(
            len(max(exclusive_to_second, key=len, default="")), max_header_length
        )

        max_length = max(
            max_header_length,
            match_max_length,
            diff_max_length1,
            diff_max_length2,
            len(title1),
            len(title2),
        )

        divider = "=" * max_length

        echo("\n", nl=False)
        echo(title1)
        echo(header1)
        echo(header2)
        echo(divider)
        for match in matches:
            echo(match)
        echo("\n", nl=False)

        echo(title2)
        echo(header1)
        echo(divider)
        for package_with_dependencies in exclusive_to_first:
            echo(package_with_dependencies)
        echo("\n", nl=False)

        echo(title2)
        echo(header2)
        echo(divider)
        for package_with_dependencies in exclusive_to_second:
            echo(f"{package_with_dependencies}")
        echo("\n", nl=False)

    if not query_result1 and not query_result2:
        echo(
            f"No records were found in the database for\n"
            f"{dist_arch_and_package_name1[0]} - "
            f"{dist_arch_and_package_name1[1]} - "
            f"{dist_arch_and_package_name1[2]}\n"
            f"{dist_arch_and_package_name2[0]} - "
            f"{dist_arch_and_package_name2[1]} - "
            f"{dist_arch_and_package_name2[2]}"
        )

    if not query_result1 and query_result2:
        print_for_one(dist_arch_and_package_name2, query_result1)

    if query_result1 and not query_result2:
        print_for_one(dist_arch_and_package_name1, query_result1)

    if query_result1 and query_result2:
        print_for_both(
            dist_arch_and_package_name1,
            query_result1,
            dist_arch_and_package_name2,
            query_result2,
        )


def print_list(data: dict[str, list[str]]) -> None:
    for section in data.keys():
        echo(f"{section.upper()}:")
        for value in sorted(data[section]):
            echo(value)
        echo("\n", nl=False)


def print_divergent(
    dist_and_arch1: tuple[str, str],
    query_result1: dict[str, list[str]],
    dist_and_arch2: tuple[str, str],
    query_result2: dict[str, list[str]],
) -> None:
    set_of_packages1 = set(query_result1.keys())
    set_of_packages2 = set(query_result2.keys())

    definitely_divergent = set.symmetric_difference(set_of_packages1, set_of_packages2)
    maybe_divergent = set_of_packages1.intersection(set_of_packages2)

    divergent_packages: list[str] = []
    for package_name in maybe_divergent:
        if sorted(query_result1[package_name]) != sorted(query_result2[package_name]):
            divergent_packages.append(package_name)

    divergent_packages.extend(definitely_divergent)

    echo(
        f"# The following packages have divergent dependencies "
        f"in {dist_and_arch1} and {dist_and_arch2}"
    )

    for package_name in divergent_packages:
        echo(package_name)

    echo("\n", nl=False)
