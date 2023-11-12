import logging
import sqlite3
from pathlib import Path
from sys import exit
from typing import Dict, List, Tuple

from depinspect import files


def remove(db_path: Path) -> None:
    file_extension = db_path.suffix
    if file_extension == ".db":
        logging.info("Removing database.")
        files.remove_file(db_path)
    else:
        logging.error(f"File specified at {db_path} is not an sqlite3 database.")
        exit(1)


def new(db_name: str, output_path: Path) -> Path:
    db_path = output_path / Path(db_name)

    if db_path.is_file() and db_path.suffix == ".db":
        logging.warning(f"sqlite3 database already exists at: {db_path}.")
        try:
            remove(db_path)
        except Exception:
            logging.exception(
                "There was an exception trying to remove existing database."
            )

    logging.info("Creating and initializing new database.")
    connection = sqlite3.connect(db_path)

    connection.execute(
        "CREATE TABLE IF NOT EXISTS Packages "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "distribution TEXT, architecture TEXT, package_name TEXT, version TEXT, "
        "UNIQUE(distribution, architecture, package_name, version))"
    )

    connection.execute(
        "CREATE TABLE IF NOT EXISTS Dependencies "
        "(package_id INTEGER, dependency_name TEXT, FOREIGN KEY (package_id) "
        "REFERENCES Packages(id))"
    )
    connection.close()
    logging.info("Successfully initialized new database.")
    return db_path


def find_dependencies(
    db_path: Path, distribution: str, package_architecture: str, package_name: str
) -> List[Tuple[str]]:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    result = db.execute(
        "SELECT dependency_name "
        "FROM Dependencies "
        "JOIN Packages ON Dependencies.package_id = Packages.id "
        "WHERE Packages.distribution = ? "
        "AND Packages.package_name = ? "
        "AND Packages.architecture = ?",
        (distribution, package_name, package_architecture),
    ).fetchall()
    db.close()
    return result


def find_all_distinct(db_path: Path) -> Dict[str, List[str]]:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

    result: Dict[str, List[str]] = {
        "distributions": [],
        "architectures": [],
        "package_names": [],
    }

    with db:
        for distribution in db.execute("SELECT DISTINCT distribution FROM Packages"):
            result["distributions"].append(distribution[0])
        for architecture in db.execute("SELECT DISTINCT architecture FROM Packages"):
            result["architectures"].append(architecture[0])
        for package_name in db.execute("SELECT DISTINCT package_name FROM Packages"):
            result["package_names"].append(package_name[0])

    db.close()

    return result


def find_packages(
    db_path: Path, distribution: str, architecture: str
) -> Dict[str, List[str]]:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

    result: Dict[str, List[str]] = {}

    with db:
        for package_id, package_name in db.execute(
            "SELECT id, package_name FROM Packages "
            "WHERE distribution = ? AND architecture = ?",
            (distribution, architecture),
        ):
            dependencies = db.execute(
                "SELECT dependency_name FROM Dependencies WHERE package_id = ?",
                (package_id,),
            ).fetchall()

            result[package_name] = dependencies[0][0]

    db.close()

    return result
