import logging
import sqlite3
from pathlib import Path
from sys import exit
from typing import List, Tuple

from click import echo

from depinspect import files


def db_remove(db_path: Path) -> None:
    """
    Remove an SQLite3 database file.

    Parameters:
    - db_path (Path): The path to the SQLite3 database file.

    Returns:
    - None

    Raises:
    - SystemExit: If the file specified is not an SQLite3 database (with a '.db' extension).

    Note:
    This function logs information and errors using the 'logging' module.
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
    Create and initialize a new SQLite3 database.

    Parameters:
    - db_name (str): The name of the new database.
    - output_path (Path): The directory where the new database will be created.

    Returns:
    - Path: The path to the newly created database.

    Raises:
    - Exception: If there is an issue removing an existing database.
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
        "CREATE TABLE IF NOT EXISTS Packages (id INTEGER PRIMARY KEY AUTOINCREMENT, distribution TEXT, architecture TEXT, package_name TEXT, version TEXT, UNIQUE(distribution, architecture, package_name, version))"
    )

    connection.execute(
        "CREATE TABLE IF NOT EXISTS Dependencies (package_id INTEGER, dependency_name TEXT, FOREIGN KEY (package_id) REFERENCES Packages(id))"
    )
    connection.close()
    logging.info("Successfully initialized new database.")
    return db_path


def db_list_dependencies(
    db_path: Path, distribution: str, package_architecture: str, package_name: str
) -> List[Tuple[str]]:
    """
    List dependencies for a specific package in an SQLite3 database.

    Parameters:
    - db_path (Path): The path to the SQLite3 database.
    - distribution (str): The distribution of the package.
    - package_architecture (str): The architecture of the package.
    - package_name (str): The name of the package.

    Returns:
    - List[Tuple[str]]: A list of tuples containing dependency names.

    Note:
    This function opens a read-only connection to the database, retrieves dependencies
    for the specified package, and returns the result as a list of tuples.
    """
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    result = db.execute(
        "SELECT dependency_name \
        FROM Dependencies \
        JOIN Packages ON Dependencies.package_id = Packages.id \
        WHERE Packages.distribution = ? AND Packages.package_name = ? AND Packages.architecture = ?",
        (distribution, package_name, package_architecture),
    ).fetchall()
    db.close()
    return result


def db_list_all(db_path: Path) -> None:
    """
    List all unique distributions, architectures, and package names in an SQLite3 database.

    Parameters:
    - db_path (Path): The path to the SQLite3 database.

    Returns:
    - None

    Note:
    This function opens a read-only connection to the database, retrieves distinct distributions,
    architectures, and package names, and prints the results.
    """
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

    with db:
        echo("Distributions:")
        echo("========================================")
        for distribution in db.execute("SELECT DISTINCT distribution FROM Packages"):
            echo(distribution[0])
        echo("\n", nl=False)
        echo("Architectures:")
        echo("========================================")
        for architecture in db.execute("SELECT DISTINCT architecture FROM Packages"):
            echo(architecture[0])
        echo("\n", nl=False)
        echo("Packages:")
        echo("========================================")
        for package_name in db.execute("SELECT DISTINCT package_name FROM Packages"):
            echo(package_name[0])

    db.close()
