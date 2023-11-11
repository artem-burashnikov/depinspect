from typing import List, Tuple

from click import echo


def print_one(package: Tuple[str, str, str], result: List[Tuple[str]]) -> None:
    """
    Print information for a single package, including its dependencies.

    Parameters:
    - package (Tuple[str, str, str]): A tuple containing distribution, architecture, and package name.
    - result (List[Tuple[str]]): A list containing tuples with dependency information.

    Returns:
    - None

    Note:
    This function takes a package tuple and its dependencies and prints the information in a formatted manner.
    It calculates the maximum character length for formatting and prints the header, divider, and dependencies.
    """
    distribution, architecture, package_name = package
    dependencies = sorted(result[0][0].split(","))
    header = f"{distribution} - {architecture} - {package_name}"

    max_char_length = (
        len(max(dependencies, key=len)) if len(dependencies) != 0 else len(header)
    )

    divider = "=" * max_char_length

    echo(header)
    echo(divider)
    for dependency in dependencies:
        echo(f"{dependency}")


def print_both(
    package1: Tuple[str, str, str],
    result1: List[Tuple[str]],
    package2: Tuple[str, str, str],
    result2: List[Tuple[str]],
) -> None:
    """
    Print information for two packages, including their dependencies and exclusions.

    Parameters:
    - package1 (Tuple[str, str, str]): A tuple containing distribution, architecture, and package name for the first package.
    - result1 (List[Tuple[str]]): A list containing tuples with dependency information for the first package.
    - package2 (Tuple[str, str, str]): A tuple containing distribution, architecture, and package name for the second package.
    - result2 (List[Tuple[str]]): A list containing tuples with dependency information for the second package.

    Returns:
    - None

    Note:
    This function takes information for two packages and their dependencies, and prints a comparison of their dependencies.
    It shows dependencies present in both, as well as exclusions for each package.
    """
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

    match_max_length = max(len(max(matches, key=len, default="")), max_header_length)

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
        len("THESE DEPENDENCIES ARE PRESENT IN BOTH"),
    )

    divider = "=" * max_length

    echo("\n", nl=False)
    echo("THESE DEPENDENCIES ARE PRESENT IN BOTH")
    echo(header1)
    echo(header2)
    echo(divider)
    for match in matches:
        echo(match)
    # echo(divider)
    echo("\n", nl=False)

    echo("THESE ARE ONLY EXCLUSIVE TO")
    echo(header1)
    echo(divider)
    for difference in differences1:
        echo(difference)
    # echo(divider)
    echo("\n", nl=False)

    echo("THESE ARE ONLY EXCLUSIVE TO")
    echo(header2)
    echo(divider)
    for difference in differences2:
        echo(f"|_ {difference}")
    echo("\n", nl=False)


def print_result(
    input1: Tuple[str, str, str],
    result_from_input1: List[Tuple[str]],
    input2: Tuple[str, str, str],
    result_from_input2: List[Tuple[str]],
) -> None:
    """
    Print the result of comparing dependencies for two input packages.

    Parameters:
    - input1 (Tuple[str, str, str]): A tuple containing distribution, architecture, and package name for the first input package.
    - result_from_input1 (List[Tuple[str]]): A list containing tuples with dependency information for the first input package.
    - input2 (Tuple[str, str, str]): A tuple containing distribution, architecture, and package name for the second input package.
    - result_from_input2 (List[Tuple[str]]): A list containing tuples with dependency information for the second input package.

    Returns:
    - None

    Note:
    This function prints the result of comparing dependencies for two input packages.
    It checks if there are records found for each input and calls the appropriate printing function.
    """
    if not result_from_input1 and not result_from_input2:
        echo(
            f"No records were found. Printing input...\n{input1[0]} - {input1[1]} - {input1[2]}\n{input2[0]} - {input2[1]} - {input2[2]}"
        )

    if not result_from_input1 and result_from_input2:
        print_one(input2, result_from_input2)

    if result_from_input1 and not result_from_input2:
        print_one(input1, result_from_input1)

    if result_from_input1 and result_from_input2:
        print_both(input1, result_from_input1, input2, result_from_input2)
