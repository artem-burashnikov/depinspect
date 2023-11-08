import logging
import sqlite3
from pathlib import Path
from sys import exit

from depinspect import files


def db_remove(db_path: Path) -> None:
    file_extension = db_path.suffix
    if file_extension == ".db":
        logging.info("Removing database.")
        files.remove_file(db_path)
    else:
        logging.error(f"File specified at {db_path} is not an sqlite3 database.")
        exit(1)


def db_new(db_name: str, output_path: Path) -> Path:
    db_path = output_path / Path(db_name)

    if db_path.is_file() and db_path.suffix == ".db":
        logging.warning(f"sqlite3 database already exists at: {db_path}.")
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


def db_select_query(
    db_path: Path, distribution: str, package_architecture: str, package_name: str
) -> None:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    with db:
        for result in db.execute(
            "SELECT distribution, architecture, package_name, version FROM Packages WHERE Packages.distribution = ? AND Packages.package_name = ? AND Packages.architecture = ?",
            (distribution, package_name, package_architecture),
        ):
            print(result)
    db.close()


"""
SELECT Dependencies.package_id, Dependencies.dependency_name
FROM Dependencies
JOIN Packages ON Dependencies.package_id = Packages.id
WHERE Packages.distribution = ? AND Packages.package_name = ? AND Packages.architecture = ?;
"""
