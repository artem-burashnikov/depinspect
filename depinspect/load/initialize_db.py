import sqlite3
import sys
from pathlib import Path
from typing import List

from depinspect.load import file_management


def execute_query_with_context(
    connection: sqlite3.Connection, query: str
) -> sqlite3.Cursor:
    """
    Executes an SQLite query within a context to ensure auto-commit on successful query

    Args:
        connection (sqlite3.Connection): SQLite database connection.
        query (str): SQLite query to be executed.

    Returns:
        sqlite3.Cursor: Result cursor of the executed query.
    """
    try:
        with connection:
            return connection.execute(query)
    except sqlite3.Error as sql_err:
        print(
            f"There was an exception executing a query:\n{sql_err}\nYour query was: '{query}'"
        )
        sys.exit(1)


def initialize_new_db() -> None:
    """
    Creates a new SQLite database named 'dependencies.db' and initializes the 'Packages' table.

    Raises:
        SystemExit: Exits the program if an exception occurs during database creation.
    """
    try:
        # Open a connection to a specified database or create new database if it doesn't exist.
        connection = sqlite3.connect("dependencies.db")

        connection.execute(
            "CREATE TABLE IF NOT EXISTS Packages (id INTEGER PRIMARY KEY, package_name TEXT, version TEXT, distribution TEXT, architecture TEXT)"
        )

        connection.execute(
            "CREATE TABLE IF NOT EXISTS Dependencies (package_id INTEGER, dependency_name TEXT, FOREIGN KEY (package_id) REFERENCES Packages(id))"
        )

        # Connection has to be manually closed.
        connection.close()
    except sqlite3.Error as sql_err:
        print(f"There was an eror trying to create a database:\n{sql_err}")
        file_management.remove_file(Path("dependencies.db"))
        sys.exit(1)


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


def process_ubuntu_metadata(file_path: Path) -> None:
    """
    Process metadata from a file into a database.

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
            version: str = ""
            architecture: List[str] = []
            depends: List[str] = []

            for line in file:
                if line.startswith("Package:"):
                    # Extract the 'Package' information
                    package = line[len("Package:") :].strip()

                elif line.startswith("Version:"):
                    # Extract the 'Version' information
                    version = line[len("Version:") :].strip()

                elif line.startswith("Architecture:"):
                    # Extract the 'Architecture' information.
                    # Several acrhitecture strings provided by a '$ dpkg-architecture -L' command
                    # COULD be listed. Usually any, all or specific.
                    parse_string_to_list(
                        string=line,
                        prefix_to_exclude="Architecture:",
                        delimiter=" ",
                        result=architecture,
                    )

                elif line.startswith("Depends:"):
                    # Extract the 'Depends' information as a list
                    parse_string_to_list(
                        string=line,
                        prefix_to_exclude="Depends:",
                        delimiter=",",
                        result=depends,
                    )

                elif line.startswith("\n"):
                    # Process previously red metadata when a blank line is encountered
                    # Why conditions are such: https://docs.python.org/3/library/stdtypes.html#truth-value-testing
                    if package and version and architecture:
                        print(
                            f"Package: {package}\nArchitecture: {architecture}\nVersion: {version}\nDepends: {depends}"
                        )
                        print("==================================================")

                    package = ""
                    version = ""
                    architecture.clear()
                    depends.clear()

    except Exception as e:
        # Handle exceptions during file reading
        print(f"Could not read a file at '{file_path}',\n{e}")
        sys.exit(1)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
