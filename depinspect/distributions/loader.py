import logging
import sqlite3
from pathlib import Path
from sys import exit

from depinspect.distributions.mapping import distribution_class_mapping
from depinspect.files import list_files_in_directory


def process_metadata_into_db(
    file_path: Path, db_path: Path, distribution: str, release: str
) -> None:
    if not file_path.is_file() or file_path.suffix != ".txt":
        logging.exception(
            f"{file_path.name} is not a valid metadata file or doesn't exist."
        )
        exit(1)

    if not db_path.is_file() or db_path.suffix != ".sqlite":
        logging.exception(
            f"{db_path.name} is not a valid sqlite3 database or doesn't exist."
        )
        exit(1)

    db_connection = sqlite3.connect(db_path)

    with db_connection:
        package_class = distribution_class_mapping[distribution]
        packages = package_class.parse_matadata(file_path, release)

        for package in packages:
            maybe_result = db_connection.execute(
                """
                SELECT name, arch, version, release
                FROM packages
                WHERE name = ?
                AND arch = ?
                AND version = ?
                AND release = ?
                """,
                (
                    package.package,
                    package.architecture,
                    package.version,
                    package.release,
                ),
            ).fetchall()

            if not maybe_result:
                result = db_connection.execute(
                    """
                    INSERT OR ABORT INTO packages
                    (name, arch, version, release, description) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        package.package,
                        package.architecture,
                        package.version,
                        package.release,
                        package.description,
                    ),
                )

                last_package_id = result.lastrowid

                db_connection.executemany(
                    """
                    INSERT INTO depends
                    (name, release, pkgKey) VALUES (?, ?, ?)
                    """,
                    (
                        [
                            (entry, package.release, last_package_id)
                            for entry in package.depends
                        ]
                    ),
                )
            else:
                continue

    logging.info(f"File {file_path.name} has been processed succesfully.")

    db_connection.close()


def deserialize_metadata(
    tmp_dir: Path, db_path: Path, distribution: str, release: str
) -> None:
    txt_files = [
        txt_file
        for txt_file in list_files_in_directory(tmp_dir)
        if txt_file.suffix == ".txt"
        and txt_file.stem.startswith(distribution)
        and release in txt_file.stem
    ]
    for file_path in txt_files:
        process_metadata_into_db(file_path, db_path, distribution, release)
