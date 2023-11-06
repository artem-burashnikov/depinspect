import logging
import sys
from pathlib import Path
from shutil import rmtree
from sqlite3 import connect
from typing import List

from depinspect.files import list_files_in_directory
from depinspect.load import sqlite_db


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


def process_metadata_into_db(file_path: Path, db_path: Path) -> None:
    if file_path.suffix != ".txt":
        logging.exception(f"{file_path.name} is not a valid metadata file.")
        sys.exit(1)

    if db_path.suffix != ".db":
        logging.exception(f"{db_path.name} is not a valid sqlite3 database.")
        sys.exit(1)

    db_connection = connect(db_path)

    with db_connection:
        with open(file_path, "r") as file:
            logging.info(f"Processing packages metadata from {file_path.name}.")
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

        logging.info(f"File {file_path.name} has been processed succesfully.")

    db_connection.close()


def run_ubuntu_metadata_processing(tmp_dir: Path, db_path: Path) -> None:
    try:
        txt_files = [
            txt_file
            for txt_file in list_files_in_directory(tmp_dir)
            if txt_file.suffix == ".txt"
        ]
        for file_path in txt_files:
            process_metadata_into_db(file_path, db_path)
    except Exception:
        logging.exception("There was an exception trying to process ubuntu metadata.")
        if db_path.is_file():
            logging.info("Removing database as it may be corrupted.")
            sqlite_db.db_remove(db_path)
    finally:
        logging.info("Cleaning up.")
        rmtree(tmp_dir)
        logging.info("Done.")
