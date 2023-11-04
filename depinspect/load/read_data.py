import sys
from pathlib import Path
from typing import List


def parse_string_to_list(
    string: str, prefix_to_exclude: str, delimiter: str, result: List[str]
) -> List[str]:
    """
    Parse a string, exclude a specified prefix, split it using a delimiter,
    and insert the resulting elements into a list.

    Args:
        string (str): The input string to be parsed.
        prefix_to_exclude (str): The prefix to exclude from the input string.
        delimiter (str): The delimiter used to split the string into elements.
        result (List[str]): The list to which the parsed elements will be inserted.

    Returns:
        List[str]: The updated list containing the parsed elements.

    Example:
        If string = "Type: A, B, C", prefix_to_exclude = "Type:", delimiter = ",", and
        result = [], the function will append ["C", "B", "A"] to result.
    """
    for entry in map(
        lambda x: x.strip(), string[len(prefix_to_exclude) :].strip().split(delimiter)
    ):
        result.insert(0, entry)
    return result


def process_metadata(file_path: Path) -> None:
    """
    Process metadata from a file.

    Args:
        file_path (Path): The path to the file to be processed.

    Raises:
        Exception: If there is an issue reading the file.

    Returns:
        None
    """
    try:
        with open(file_path, "r") as file:
            package: str = ""
            architecture: List[str] = []
            version: str = ""
            depends: List[str] = []
            recommends: List[str] = []

            for line in file:
                if line.startswith("Package:"):
                    # Extract the 'Package' information
                    package = line[len("Package:") :].strip()

                elif line.startswith("Architecture:"):
                    # Extract the 'Architecture' information.
                    # Several acrhitecture strings provided by a '$ dpkg-architecture -L' command
                    # could be listed.
                    parse_string_to_list(
                        string=line,
                        prefix_to_exclude="Architecture:",
                        delimiter=" ",
                        result=architecture,
                    )

                elif line.startswith("Version:"):
                    # Extract the 'Version' information
                    version = line[len("Version:") :].strip()

                elif line.startswith("Depends:"):
                    # Extract the 'Depends' information as a list
                    parse_string_to_list(
                        string=line,
                        prefix_to_exclude="Depends:",
                        delimiter=",",
                        result=depends,
                    )

                elif line.startswith("Recommends:"):
                    # Extract the 'Recommends' information as a list
                    parse_string_to_list(
                        string=line,
                        prefix_to_exclude="Recommends:",
                        delimiter=",",
                        result=recommends,
                    )

                elif line.startswith("\n"):
                    # Process metadata when a blank line is encountered
                    if len(package) != 0:
                        print(
                            f"Package: {package}\nArchitecture: {architecture}\nVersion: {version}\nDepends: {depends}\nRecommends: {recommends}"
                        )
                        print("==================================================")

                    package = ""
                    architecture.clear()
                    version = ""
                    depends.clear()
                    recommends.clear()

    except Exception as e:
        # Handle exceptions during file reading
        print(f"Could not read a file at '{file_path}',\n{e}")
        sys.exit(1)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
