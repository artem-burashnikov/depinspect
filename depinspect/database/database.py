import logging
import sqlite3
from pathlib import Path


def init(db_name: str, output_path: Path) -> Path:
    """Initialize a SQLite database for package metadata.

    Parameters
    ----------
    db_name : str
        Name of the SQLite database.
    output_path : Path
        Path to the directory where the database will be created.

    Returns
    -------
    Path
        Path to the initialized SQLite database.
    """
    db_path = output_path / Path(db_name)

    logging.info("Initializing a database.")
    con = sqlite3.connect(db_path)

    con.executescript(
        """
        BEGIN;
        DROP TABLE IF EXISTS packages;
        DROP TABLE IF EXISTS depends;
        DROP TABLE IF EXISTS recommends;
        DROP TABLE IF EXISTS suggests;
        DROP TABLE IF EXISTS enhances;
        DROP TABLE IF EXISTS breaks;
        DROP TABLE IF EXISTS conflicts;
        DROP TABLE IF EXISTS provides;
        CREATE TABLE packages
            (  pkgKey INTEGER PRIMARY KEY,  pkgId TEXT,  name TEXT, arch TEXT,
                version TEXT,  release TEXT,  description TEXT  );
        CREATE TABLE depends
            (  name TEXT,  version TEXT,  release TEXT,
               pkgKey INTEGER , pre BOOLEAN DEFAULT FALSE  );
        CREATE TABLE recommends
            (  name TEXT,  version TEXT,  release TEXT,
               pkgKey INTEGER  );
        CREATE TABLE suggests
            (  name TEXT,  version TEXT,  release TEXT,
               pkgKey INTEGER  );
        CREATE TABLE enhances
            (  name TEXT,  version TEXT,  release TEXT,
               pkgKey INTEGER  );
        CREATE TABLE breaks
            (  name TEXT,  version TEXT,  release TEXT,
               pkgKey INTEGER  );
        CREATE TABLE conflicts
            (  name TEXT,  version TEXT,  release TEXT,
               pkgKey INTEGER  );
        CREATE TABLE provides
            (  name TEXT,  version TEXT,  release TEXT,
               pkgKey INTEGER  );
        CREATE INDEX packagename ON packages (name);
        CREATE INDEX packageId ON packages (pkgId);
        CREATE INDEX pkgdepends on depends (pkgKey);
        CREATE INDEX dependsname ON depends (name);
        CREATE INDEX pkgprovides on provides (pkgKey);
        CREATE INDEX providesname ON provides (name);
        CREATE INDEX pkgconflicts on conflicts (pkgKey);
        CREATE INDEX pkgsuggests on suggests (pkgKey);
        CREATE INDEX pkgenhances on enhances (pkgKey);
        CREATE INDEX pkgrecommends on recommends (pkgKey);
        COMMIT;
        """
    )

    con.close()
    logging.info("Successfully initialized a database.")
    return db_path


def find_dependencies(
    db_con: sqlite3.Connection, table: str, arch: str, name: str
) -> set[str]:
    """Find dependencies in an SQLite database.

    Parameters
    ----------
    db_con : sqlite3.Connection
        SQLite database connection.
    table : str
        Name of the table in the database.
    arch : str
        Architecture to search for in the 'packages' table.
    name : str
        Package name to search for in the 'packages' table.

    Returns
    -------
    set[str]
        Set of package names that the specified package depends on.

    Raises
    ------
    ValueError
        If the provided table name is not a valid SQLite table.
    """
    from depinspect.validator import is_valid_sql_table

    db_con.row_factory = sqlite3.Row

    if not is_valid_sql_table(db_con, table):
        db_con.close()
        logging.exception("%s is not a correct sqlite table name.", table)
        raise ValueError

    res = db_con.execute(
        """
        SELECT {0}.name FROM {0} JOIN packages ON {0}.pkgKey = packages.pkgKey
        WHERE packages.name = ? AND packages.arch = ?
        """.format(
            table
        ),
        (name, arch),
    ).fetchall()

    return {elem["name"] for elem in res}


def find_all_distinct(db_con: sqlite3.Connection, arch: str) -> set[str]:
    """Find all distinct package names in an SQLite database.

    Parameters
    ----------
    db_con : sqlite3.Connection
        SQLite database connection.
    arch : str
        Architecture to filter the distinct package names.

    Returns
    -------
    set[str]
        Set of distinct package names for the specified architecture.
    """
    db_con.row_factory = sqlite3.Row

    res: set[str] = set()

    with db_con:
        for row in db_con.execute(
            "SELECT DISTINCT name FROM packages WHERE arch = ?", (arch,)
        ):
            res.add(row["name"])

    return res
