import sqlite3
import sys
from pathlib import Path

from depinspect.load import files


def new() -> None:
    """
    Creates a new SQLite database named 'dependencies.db' and initializes pre-defined tables.

    Raises:
        SystemExit: Exits the program if an exception occurs during database creation.
    """
    try:
        # Open a connection to a specified database or create new database if it doesn't exist.
        connection = sqlite3.connect("dependencies.db")

        connection.execute(
            "CREATE TABLE IF NOT EXISTS Packages (id INTEGER PRIMARY KEY AUTOINCREMENT, package_name TEXT, version TEXT, distribution TEXT, architecture TEXT)"
        )

        connection.execute(
            "CREATE TABLE IF NOT EXISTS Dependencies (package_id INTEGER, dependency_name TEXT, FOREIGN KEY (package_id) REFERENCES Packages(id))"
        )
    except sqlite3.Error as sql_err:
        print(f"There was an eror trying to create a database:\n{sql_err}")
        if Path("dependencies.db").exists():
            files.remove_file(Path("dependencies.db"))
        sys.exit(1)
    finally:
        connection.close()


def main() -> None:
    pass


"""
SELECT Dependencies.package_id, Dependencies.dependency_name
FROM Dependencies
JOIN Packages ON Dependencies.package_id = Packages.id
WHERE Packages.distribution = ? AND Packages.package_name = ? AND Packages.architecture = ?;
"""

if __name__ == "__main__":
    main()
