from pathlib import Path
from shutil import rmtree
from sqlite3 import Connection, connect
from typing import List

from depinspect.load import extract, files, sqlite_db

ARCH_ALL_ANY = ["i386", "amd64", "riscv64"]


def parse_string_to_list(
    string: str, prefix_to_exclude: str, delimiter: str, result: List[str]
) -> List[str]:
    """
    Parse a string, exclude a specified prefix, split it using a delimiter,
    and append the resulting elements to a list.

    Args:
        string (str): The input string to be parsed.
        prefix_to_exclude (str): The prefix to exclude from the input string.
        delimiter (str): The delimiter used to split the string into elements.
        result (List[str]): The list to which the parsed elements will be appended to.

    Returns:
        List[str]: The updated list containing the parsed elements.

    Example:
        If string = "Type: A, B, C", prefix_to_exclude = "Type:", delimiter = ",", and
        result = [], the function will append ["A", "B", "C"] to result.
    """
    for entry in map(
        lambda x: x.strip(), string[len(prefix_to_exclude) :].strip().split(delimiter)
    ):
        result.append(entry)

    return result


def process_metadata(file_path: Path, db_connection: Connection) -> None:
    with db_connection:
        with open(file_path, "r") as file:
            print(f"Processing packages metadata from {file_path}.\nPlease wait")
            package_name: str = ""
            version: str = ""
            architecture: List[str] = []
            depends: List[str] = []

            for line in file:
                if line.startswith("Package:"):
                    # Extract the 'Package' information
                    package_name = line[len("Package:") :].strip()

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
                    if package_name and version and architecture:
                        result = db_connection.execute(
                            "INSERT INTO Packages (package_name, version, distribution, architecture) VALUES (?, ?, ?, ?)",
                            (
                                package_name,
                                version,
                                "ubuntu",
                                "".join(architecture),
                            ),
                        )
                        db_connection.execute(
                            "INSERT INTO Dependencies (package_id, dependency_name) VALUES (?, ?)",
                            (result.lastrowid, ",".join(depends)),
                        )

                    package_name = ""
                    version = ""
                    architecture.clear()
                    depends.clear()

        print(f"File {file_path} has been processed succesfully.")

    db_connection.close()


def main() -> None:
    tmp_dir = extract.main()

    if Path("dependencies.db").is_file():
        files.remove_file(Path("dependencies.db"))

    sqlite_db.new()

    db = connect("dependencies.db")

    try:
        for file_path in files.list_files_in_directory(tmp_dir):
            process_metadata(file_path, db)
    except Exception as e:
        db.close()
        print(f"{e}")
        if Path("dependencies.db").is_file():
            print("Removing database")
            files.remove_file(Path("dependencies.db"))
    finally:
        print("Closing database connection")
        db.close()
        print("Cleaning up temporary files and directory")
        rmtree(tmp_dir)


if __name__ == "__main__":
    main()
