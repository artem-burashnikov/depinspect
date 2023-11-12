from typing import Dict, List, Tuple

from click import echo


def print_diff(
    input1: Tuple[str, str, str],
    result_from_input1: List[Tuple[str]],
    input2: Tuple[str, str, str],
    result_from_input2: List[Tuple[str]],
) -> None:
    def print_result_for_one(
        package: Tuple[str, str, str], result: List[Tuple[str]]
    ) -> None:
        distribution, architecture, package_name = package
        dependencies = sorted(result[0][0].split(","))
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

    def print_result_for_both(
        package1: Tuple[str, str, str],
        result1: List[Tuple[str]],
        package2: Tuple[str, str, str],
        result2: List[Tuple[str]],
    ) -> None:
        distribution1, architecture1, package_name1 = package1
        dependencies1 = sorted(result1[0][0].split(","))
        header1 = f"{distribution1} - {architecture1} - {package_name1}"

        distribution2, architecture2, package_name2 = package2
        dependencies2 = sorted(result2[0][0].split(","))
        header2 = f"{distribution2} - {architecture2} - {package_name2}"

        matches = sorted(set(dependencies1).intersection(dependencies2))
        differences1 = sorted(set(dependencies1).difference(set(dependencies2)))
        differences2 = sorted(set(dependencies2).difference(set(dependencies1)))

        max_header_length = len(max(header1, header2, key=len))

        match_max_length = max(
            len(max(matches, key=len, default="")), max_header_length
        )

        diff_max_length1 = max(
            len(max(differences1, key=len, default="")), max_header_length
        )

        diff_max_length2 = max(
            len(max(differences2, key=len, default="")), max_header_length
        )

        max_length = max(
            max_header_length,
            match_max_length,
            diff_max_length1,
            diff_max_length2,
            len("These dependencies are present in both"),
        )

        divider = "=" * max_length

        echo("\n", nl=False)
        echo("These dependencies are present in both:")
        echo(header1)
        echo(header2)
        echo(divider)
        for match in matches:
            echo(match)
        echo("\n", nl=False)

        echo("These dependencies are exclusive to:")
        echo(header1)
        echo(divider)
        for difference in differences1:
            echo(difference)
        echo("\n", nl=False)

        echo("These dependencies are exclusive to:")
        echo(header2)
        echo(divider)
        for difference in differences2:
            echo(f"{difference}")
        echo("\n", nl=False)

    if not result_from_input1 and not result_from_input2:
        echo(
            f"No records were found. Printing input...\n"
            f"{input1[0]} - {input1[1]} - {input1[2]}\n"
            f"{input2[0]} - {input2[1]} - {input2[2]}"
        )

    if not result_from_input1 and result_from_input2:
        print_result_for_one(input2, result_from_input2)

    if result_from_input1 and not result_from_input2:
        print_result_for_one(input1, result_from_input1)

    if result_from_input1 and result_from_input2:
        print_result_for_both(input1, result_from_input1, input2, result_from_input2)


def print_list(data: Dict[str, List[str]]) -> None:
    for section in data.keys():
        echo(f"{section.upper()}:")
        for value in sorted(data[section]):
            print(value)
        echo("\n", nl=False)


def print_divergent(
    dist_and_arch1: Tuple[str, str],
    result1: Dict[str, List[str]],
    dist_and_arch2: Tuple[str, str],
    result2: Dict[str, List[str]],
) -> None:
    result: List[str] = []

    set_of_packages1 = set(key for key in result1.keys())
    set_of_packages2 = set(key for key in result2.keys())

    definitely_diverge = set.symmetric_difference(set_of_packages1, set_of_packages2)
    maybe_diverge = set_of_packages1.intersection(set_of_packages2)

    for package_name in maybe_diverge:
        if sorted(result1[package_name]) != sorted(result2[package_name]):
            result.append(package_name)

    result.extend(definitely_diverge)

    echo(
        f"# The following packages have divergent dependencies "
        f"in {dist_and_arch1} and {dist_and_arch2}"
    )

    for item in sorted(result):
        echo(item)

    echo("\n", nl=False)
