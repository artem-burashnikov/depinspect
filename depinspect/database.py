import logging
import sqlite3
from pathlib import Path
from sys import exit

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

    logging.info("Initializing a database.")
    connection = sqlite3.connect(db_path)

    connection.executescript(
        """
        BEGIN;
        DROP TABLE IF EXISTS packages;
        DROP TABLE IF EXISTS dependencies;
        CREATE TABLE packages
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            distribution TEXT, architecture TEXT, package_name TEXT, version TEXT,
            UNIQUE(distribution, architecture, package_name, version));
        CREATE TABLE dependencies
            (package_id INTEGER, dependency_name TEXT, FOREIGN KEY (package_id)
            REFERENCES Packages(id));
        COMMIT;
    """
    )

    connection.close()
    logging.info("Successfully initialized a database.")
    return db_path


def find_dependencies(
    db_path: Path, distribution: str, package_architecture: str, package_name: str
) -> list[tuple[str]]:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    result = db.execute(
        "SELECT dependency_name "
        "FROM dependencies "
        "JOIN packages ON dependencies.package_id = packages.id "
        "WHERE packages.distribution = ? "
        "AND packages.package_name = ? "
        "AND packages.architecture = ?",
        (distribution, package_name, package_architecture),
    ).fetchall()
    db.close()
    return result


def find_all_distinct(db_path: Path) -> dict[str, list[str]]:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

    result: dict[str, list[str]] = {
        "distributions": [],
        "architectures": [],
        "package_names": [],
    }

    with db:
        for distribution in db.execute("SELECT DISTINCT distribution FROM packages"):
            result["distributions"].append(distribution[0])
        for architecture in db.execute("SELECT DISTINCT architecture FROM packages"):
            result["architectures"].append(architecture[0])
        for package_name in db.execute("SELECT DISTINCT package_name FROM packages"):
            result["package_names"].append(package_name[0])

    db.close()

    return result


def find_packages(
    db_path: Path, distribution: str, architecture: str
) -> dict[str, list[str]]:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

    result: dict[str, list[str]] = {}

    with db:
        for package_id, package_name in db.execute(
            "SELECT id, package_name FROM packages "
            "WHERE distribution = ? AND architecture = ?",
            (distribution, architecture),
        ):
            dependencies = db.execute(
                "SELECT dependency_name FROM dependencies WHERE package_id = ?",
                (package_id,),
            ).fetchall()

            result[package_name] = dependencies[0][0]

    db.close()

    return result
