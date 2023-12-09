import logging
import sqlite3
from pathlib import Path
from sys import exit

from depinspect.distributions.package import Package
from depinspect.files import list_files_in_directory


def validate_metadata_file_exists(file_path: Path) -> None:
    if not file_path.is_file() or file_path.suffix != ".txt":
        logging.exception(
            "%s is not a valid metadata file or doesn't exist.", file_path.name
        )
        exit(1)


def valid_database_file_exists(db_path: Path) -> None:
    if not db_path.is_file() or db_path.suffix != ".sqlite":
        logging.exception(
            "%s is not a valid sqlite3 database or doesn't exist.", db_path.name
        )
        exit(1)


def is_not_in_db(db_connection: sqlite3.Connection, pkg: Package) -> bool:
    res = db_connection.execute(
        """SELECT name, arch, version, release FROM packages
        WHERE name = ? AND arch = ? AND version = ? AND release = ?""",
        (pkg.package, pkg.architecture, pkg.version, pkg.release),
    )

    return True if res.fetchone() is None else False


def insert_into_packages(db_connection: sqlite3.Connection, pkg: Package) -> int:
    res = db_connection.execute(
        """INSERT INTO packages (name, arch, version, release, description)
        VALUES (?, ?, ?, ?, ?)""",
        (pkg.package, pkg.architecture, pkg.version, pkg.release, pkg.description),
    )

    if not res.lastrowid:
        logging.exception(
            "Failed to insert row into database. "
            "Values that caused an error: %s, %s, %s, %s, %s",
            pkg.package,
            pkg.architecture,
            pkg.version,
            pkg.release,
        )
        db_connection.close()
        exit(1)

    return res.lastrowid


def map_additional_info(
    input_list: list[str], release: str, key: int
) -> list[tuple[str, str, int]]:
    return [(entry, release, key) for entry in input_list]


def insert_into_depends(
    db_connection: sqlite3.Connection, pkg: Package, pkg_key: int
) -> None:
    if pkg.depends:
        db_connection.executemany(
            """INSERT INTO depends (name, release, pkgKey)
            VALUES (?, ?, ?)""",
            (map_additional_info(pkg.depends, pkg.release, pkg_key)),
        )


def insert_into_recommends(
    db_connection: sqlite3.Connection, pkg: Package, pkg_key: int
) -> None:
    if pkg.recommends:
        db_connection.executemany(
            """INSERT INTO recommends (name, release, pkgKey)
            VALUES (?, ?, ?)""",
            (map_additional_info(pkg.recommends, pkg.release, pkg_key)),
        )


def insert_into_suggests(
    db_connection: sqlite3.Connection, pkg: Package, pkg_key: int
) -> None:
    if pkg.suggests:
        db_connection.executemany(
            """INSERT INTO suggests (name, release, pkgKey)
            VALUES (?, ?, ?)""",
            (map_additional_info(pkg.suggests, pkg.release, pkg_key)),
        )


def insert_into_enhances(
    db_connection: sqlite3.Connection, pkg: Package, pkg_key: int
) -> None:
    if pkg.enhances:
        db_connection.executemany(
            """INSERT INTO enhances (name, release, pkgKey)
            VALUES (?, ?, ?)""",
            (map_additional_info(pkg.enhances, pkg.release, pkg_key)),
        )


def insert_into_breaks(
    db_connection: sqlite3.Connection, pkg: Package, pkg_key: int
) -> None:
    if pkg.breaks:
        db_connection.executemany(
            """INSERT INTO breaks (name, release, pkgKey)
            VALUES (?, ?, ?)""",
            (map_additional_info(pkg.breaks, pkg.release, pkg_key)),
        )


def insert_into_conflicts(
    db_connection: sqlite3.Connection, pkg: Package, pkg_key: int
) -> None:
    if pkg.conflicts:
        db_connection.executemany(
            """INSERT INTO conflicts (name, release, pkgKey)
            VALUES (?, ?, ?)""",
            (map_additional_info(pkg.conflicts, pkg.release, pkg_key)),
        )


def insert_into_provides(
    db_connection: sqlite3.Connection, pkg: Package, pkg_key: int
) -> None:
    if pkg.provides:
        db_connection.executemany(
            """INSERT INTO provides (name, release, pkgKey)
            VALUES (?, ?, ?)""",
            (map_additional_info(pkg.provides, pkg.release, pkg_key)),
        )


def process_metadata_into_db(
    file_path: Path, db_path: Path, distribution: str, release: str
) -> None:
    from depinspect.distributions.mapping import distribution_class_mapping

    validate_metadata_file_exists(file_path)
    valid_database_file_exists(db_path)

    db_connection = sqlite3.connect(db_path)

    with db_connection:
        package_class = distribution_class_mapping[distribution]
        packages = package_class.parse_metadata(file_path, release)

        for pkg in packages:
            if is_not_in_db(db_connection, pkg):
                pkg_key = insert_into_packages(db_connection, pkg)
                insert_into_depends(db_connection, pkg, pkg_key)
                insert_into_recommends(db_connection, pkg, pkg_key)
                insert_into_suggests(db_connection, pkg, pkg_key)
                insert_into_enhances(db_connection, pkg, pkg_key)
                insert_into_breaks(db_connection, pkg, pkg_key)
                insert_into_conflicts(db_connection, pkg, pkg_key)
                insert_into_provides(db_connection, pkg, pkg_key)
            else:
                continue

    logging.info("File %s has been processed succesfully.", file_path.name)

    db_connection.close()


def deserialize_ubuntu_metadata(
    tmp_dir: Path, db_path: Path, distribution: str, release: str
) -> None:
    txt_files = [
        txt_file
        for txt_file in list_files_in_directory(tmp_dir)
        if txt_file.suffix == ".txt"
        and txt_file.stem.startswith(distribution)
        and release in txt_file.stem
    ]
    for file_path in txt_files:
        process_metadata_into_db(file_path, db_path, distribution, release)
