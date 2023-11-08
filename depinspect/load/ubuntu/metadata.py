import logging
from pathlib import Path
from sqlite3 import connect
from sys import exit
from typing import List

from depinspect.files import list_files_in_directory


def parse_string_to_list(
    string: str, prefix_to_exclude: str, delimiter: str, result: List[str]
) -> List[str]:
    for entry in map(
        lambda x: x.strip(), string[len(prefix_to_exclude) :].strip().split(delimiter)
    ):
        result.append(entry)

    return result


def process_metadata_into_db(file_path: Path, db_path: Path) -> None:
    if file_path.suffix != ".txt":
        logging.exception(f"{file_path.name} is not a valid metadata file.")
        exit(1)

    if db_path.suffix != ".db":
        logging.exception(f"{db_path.name} is not a valid sqlite3 database.")
        exit(1)

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
                    package_name = line[len("Package:") :].strip()

                elif line.startswith("Version:"):
                    version = line[len("Version:") :].strip()

                elif line.startswith("Architecture:"):
                    parse_string_to_list(
                        string=line,
                        prefix_to_exclude="Architecture:",
                        delimiter=" ",
                        result=architecture,
                    )

                elif line.startswith("Depends:"):
                    parse_string_to_list(
                        string=line,
                        prefix_to_exclude="Depends:",
                        delimiter=",",
                        result=depends,
                    )

                elif line.startswith("\n"):
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
    txt_files = [
        txt_file
        for txt_file in list_files_in_directory(tmp_dir)
        if txt_file.suffix == ".txt" and txt_file.stem.startswith("ubuntu")
    ]
    for file_path in txt_files:
        process_metadata_into_db(file_path, db_path)
