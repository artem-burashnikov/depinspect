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
    connection = sqlite3.connect(db_path)

    connection.executescript(
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

    connection.close()
    logging.info("Successfully initialized a database.")
    return db_path


def find_dependencies(db_path: Path, table: str, arch: str, name: str) -> list[str]:
    from depinspect.validator import is_valid_sql_table

    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

    db.row_factory = sqlite3.Row

    if not is_valid_sql_table(db, table):
        db.close()
        logging.exception("%s is not a correct sqlite table name.", table)
        raise ValueError

    result = db.execute(
        """
        SELECT {0}.name FROM {0} JOIN packages ON {0}.pkgKey = packages.pkgKey
        WHERE packages.name = ? AND packages.arch = ?
        """.format(
            table
        ),
        (name, arch),
    ).fetchall()

    db.close()

    return [elem["name"] for elem in result]


def find_all_distinct(db_path: Path) -> set[str]:
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row

    result: set[str] = set()

    with db:
        for row in db.execute("SELECT DISTINCT name FROM packages"):
            result.add(row["name"])
    db.close()

    return result


# def find_dependencies(
#     db_path: Path, distribution: str, architecture: str
# ) -> dict[str, list[str]]:
#     db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

#     result: dict[str, list[str]] = {}

#     with db:
#         for package_id, package_name in db.execute(
#             "SELECT id as id, package_name as package_name FROM packages "
#             "WHERE distribution = ? AND architecture = ?",
#             (distribution, architecture),
#         ):
#             dependencies = (
#                 db.execute(
#                     "SELECT dependency_name as dependency_name "
#                     "FROM dependencies WHERE package_id = ?",
#                     (package_id,),
#                 )
#                 .fetchone()
#                 .keys()
#             )

#             result[package_name] = dependencies[0][0]

#     db.close()

#     return result
