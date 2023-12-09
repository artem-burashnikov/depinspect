import logging
import sqlite3
from pathlib import Path


def init(db_name: str, output_path: Path) -> Path:
    """
    Initialize a SQLite database for package metadata.

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


# def find_dependencies(
#     db_path: Path, distribution: str, package_architecture: str, package_name: str
# ) -> Any:
#     db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
#     db.row_factory = sqlite3.Row

#     result = db.execute(
#         "SELECT dependency_name AS name "
#         "FROM dependencies "
#         "JOIN packages ON dependencies.package_id = packages.id "
#         "WHERE packages.distribution = ? "
#         "AND packages.package_name = ? "
#         "AND packages.architecture = ?",
#         (distribution, package_name, package_architecture),
#     ).fetchall()
#     db.close()
#     return result["name"]


# def find_all_distinct(db_path: Path) -> dict[str, list[str]]:
#     db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

#     result: dict[str, list[str]] = {
#         "distributions": [],
#         "architectures": [],
#         "package_names": [],
#     }

#     with db:
#         for distribution in db.execute("SELECT DISTINCT distribution FROM packages"):
#             result["distributions"].append(distribution[0])
#         for architecture in db.execute("SELECT DISTINCT architecture FROM packages"):
#             result["architectures"].append(architecture[0])
#         for package_name in db.execute("SELECT DISTINCT package_name FROM packages"):
#             result["package_names"].append(package_name[0])

#     db.close()

#     return result


# def find_packages(
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
