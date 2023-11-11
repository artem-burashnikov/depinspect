import logging
import sqlite3
from pathlib import Path
from sys import exit

from depinspect.definitions import distribution_class_mapping
from depinspect.files import list_files_in_directory


def process_metadata_into_db(file_path: Path, db_path: Path, distribution: str) -> None:
    if not file_path.is_file() or file_path.suffix != ".txt":
        logging.exception(
            f"{file_path.name} is not a valid metadata file or doesn't exist."
        )
        exit(1)

    if not db_path.is_file() or db_path.suffix != ".db":
        logging.exception(
            f"{db_path.name} is not a valid sqlite3 database or doesn't exist."
        )
        exit(1)

    db_connection = sqlite3.connect(db_path)

    with db_connection:
        package_class = distribution_class_mapping[distribution]
        packages = package_class.parse_matadata(file_path)

        for package in packages:
            maybe_result = db_connection.execute(
                "SELECT distribution, architecture, package_name "
                "FROM Packages "
                "WHERE distribution = ? "
                "AND architecture = ? "
                "AND package_name = ?",
                (package.distribution, package.architecture, package.package),
            ).fetchall()

            if not maybe_result:
                result = db_connection.execute(
                    "INSERT OR ABORT INTO Packages "
                    "(distribution, architecture, package_name) VALUES (?, ?, ?)",
                    (package.distribution, package.architecture, package.package),
                )
                db_connection.execute(
                    "INSERT INTO Dependencies "
                    "(package_id, dependency_name) VALUES (?, ?)",
                    (result.lastrowid, ",".join(package.depends)),
                )
            else:
                continue

    logging.info(f"File {file_path.name} has been processed succesfully.")

    db_connection.close()


def run_metadata_processing(tmp_dir: Path, db_path: Path, distribution: str) -> None:
    txt_files = [
        txt_file
        for txt_file in list_files_in_directory(tmp_dir)
        if txt_file.suffix == ".txt" and txt_file.stem.startswith(distribution)
    ]
    for file_path in txt_files:
        process_metadata_into_db(file_path, db_path, distribution)
