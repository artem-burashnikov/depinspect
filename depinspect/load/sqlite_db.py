import logging
import sqlite3
from pathlib import Path

from depinspect import files


def db_remove(db_path: Path) -> bool:
    file_extension = db_path.suffix
    if file_extension == ".db":
        logging.info("Removing database.")
        files.remove_file(db_path)
        logging.info("Successfully removed database.")
        return True
    logging.warning(f"File specified at {db_path} is not an sqlite3 database.")
    return False


def db_new(db_name: str, output_path: Path) -> Path:
    db_path = Path.joinpath(output_path, Path(f"{db_name}"))

    if db_path.is_file():
        logging.warning(f"sqlite3 database alread exists at: {db_path}.")
        try:
            db_remove(db_path)
        except Exception:
            logging.exception(
                "There was an exception trying to remove existing database."
            )

    logging.info("Creating and initializing new database.")
    connection = sqlite3.connect(db_path)

    connection.execute(
        "CREATE TABLE IF NOT EXISTS Packages (id INTEGER PRIMARY KEY AUTOINCREMENT, package_name TEXT, version TEXT, distribution TEXT, architecture TEXT)"
    )

    connection.execute(
        "CREATE TABLE IF NOT EXISTS Dependencies (package_id INTEGER, dependency_name TEXT, FOREIGN KEY (package_id) REFERENCES Packages(id))"
    )
    connection.close()
    logging.info("Successfully initialized new database.")
    return db_path


"""
SELECT Dependencies.package_id, Dependencies.dependency_name
FROM Dependencies
JOIN Packages ON Dependencies.package_id = Packages.id
WHERE Packages.distribution = ? AND Packages.package_name = ? AND Packages.architecture = ?;
"""
