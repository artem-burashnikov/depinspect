import logging
import sqlite3
from pathlib import Path
from sys import exit

from depinspect import files


def db_remove(db_path: Path) -> None:
    """
    Removes an SQLite3 database file specified by the given path.

    Args:
    - db_path (Path): The path to the SQLite3 database file.

    Returns:
    bool: True if the database file was successfully removed, False otherwise.

    Notes:
    - The function checks if the file extension is ".db" before attempting to remove it.
    """
    file_extension = db_path.suffix
    if file_extension == ".db":
        logging.info("Removing database.")
        files.remove_file(db_path)
    else:
        logging.error(f"File specified at {db_path} is not an sqlite3 database.")
        exit(1)


def db_new(db_name: str, output_path: Path) -> Path:
    """
    Creates a new SQLite3 database with the specified name and path, initializing pre-defined tables.

    Args:
    - db_name (str): The name of the new SQLite3 database.
    - output_path (Path): The directory where the new database will be created.

    Returns:
    Path: A Path object representing the path to the newly created database.

    Notes:
    - If a database with the same name exists, it is removed before creating a new one.
    - Two tables, 'Packages' and 'Dependencies', are created with necessary columns.
    """
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


"""
SELECT Dependencies.package_id, Dependencies.dependency_name
FROM Dependencies
JOIN Packages ON Dependencies.package_id = Packages.id
WHERE Packages.distribution = ? AND Packages.package_name = ? AND Packages.architecture = ?;
"""
