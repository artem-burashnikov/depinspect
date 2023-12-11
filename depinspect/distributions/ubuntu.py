import logging
import sqlite3
from pathlib import Path
from re import split

from depinspect.archives.extractor import (
    extract_xz_archive,
    process_archives,
)
from depinspect.archives.fetcher import fetch_and_save_metadata
from depinspect.constants import DATABASE_DIR, DB_SUFFIX, UBUNTU_ARCHS
from depinspect.database import database
from depinspect.distributions.loader import deserialize_ubuntu_metadata
from depinspect.distributions.package import Package
from depinspect.files import list_files_in_directory


class Ubuntu(Package):
    @staticmethod
    def parse_metadata(file_path: Path, dist_release: str) -> list["Package"]:
        """Parse Ubuntu metadata file and return a list of Package objects.

        Parameters
        ----------
        file_path : Path
            Path to the Ubuntu metadata file to be parsed.
        dist_release : str
            The release name.

        Returns
        -------
        List[Package]
            A list of Package objects representing Ubuntu packages.
        """
        with open(file_path, encoding="utf-8") as file:
            file_content = file.read()
            ubuntu_packages: list[Package] = []

            blocks = split(r"\n(?=Package:)", file_content)
            for block in blocks:
                if block.strip():
                    lines = block.strip().split("\n")
                    package_info = Ubuntu()

                    for line in lines:
                        key, value = split(r":\s*", line, 1)
                        try:
                            setattr(package_info, key.lower().replace("-", "_"), value)
                        except AttributeError:
                            logging.warning(
                                "Ubuntu package field %s was not set. "
                                "Skipping value: %s",
                                key,
                                value,
                            )
                            pass

                    package_info.release = dist_release
                    ubuntu_packages.append(package_info)

        return ubuntu_packages

    @staticmethod
    def init(
        tmp_dir: Path,
        config: dict[str, dict[str, dict[str, dict[str, str]]]],
        db_suffix: str,
        output_path: Path,
    ) -> None:
        """Initialize the Ubuntu database.

        Parameters
        ----------
        tmp_dir : Path
            Temporary directory to store intermediate files.
        config : Dict[str, Dict[str, Dict[str, Dict[str, str]]]]
            Configuration dictionary containing information about sources.
        db_suffix : str
            Suffix to be added to the database name.
        output_path : Path
            Output path for the initialized database.

        Returns
        -------
        None
        """
        try:
            for release in config["ubuntu"].keys():
                logging.info("Fetching ubuntu archives.")
                fetch_and_save_metadata(config, "ubuntu", tmp_dir)

                logging.info("Extracting ubuntu xz archives.")
                process_archives(
                    input_dir=tmp_dir,
                    output_dir=tmp_dir,
                    file_extension=".txt",
                    archive_extension=".xz",
                    extractor=extract_xz_archive,
                )

                logging.info("Processing metadata into ubuntu database.")
                db_path = database.init(
                    db_name=f"ubuntu_{release}{db_suffix}", output_path=output_path
                )
                deserialize_ubuntu_metadata(tmp_dir, db_path, "ubuntu", release)
        except Exception:
            logging.exception(
                "There was an exception trying to initialize ubuntu database."
            )

    @staticmethod
    def get_all_archs() -> set[str]:
        """Get the set of all Ubuntu architectures."""
        return UBUNTU_ARCHS

    @staticmethod
    def get_stored_packages() -> set[str]:
        """Get the set of all distinct package names stored in Ubuntu databases.

        Returns
        -------
        set[str]
            Set containing all distinct package names stored in Ubuntu databases.
        """
        res: set[str] = set()

        databases = list_files_in_directory(DATABASE_DIR / "ubuntu")

        for db_path in databases:
            db_con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

            for arch in Ubuntu.get_all_archs():
                res.update(database.find_all_distinct(db_con, arch))

            db_con.close()

        return res

    @staticmethod
    def get_dependencies(arch: str, pkg: str) -> set[str]:
        """Get the dependencies of a package for a specific architecture in Ubuntu.

        Parameters
        ----------
        arch : str
            The target architecture for which dependencies are retrieved.
        pkg : str
            The name of the package for which dependencies are retrieved.

        Returns
        -------
        set[str]
            Set of dependencies of the specified package for the given architecture.

        Note
        ----
        The release version is set to "jammy".
        """
        from depinspect.validator import db_not_exists

        release = "jammy"

        db = DATABASE_DIR / "ubuntu" / f"ubuntu_{release}{DB_SUFFIX}"

        if db_not_exists(db):
            return set()

        db_con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)

        res = database.find_dependencies(
            db_con=db_con,
            table="depends",
            arch=arch,
            name=pkg,
        )

        db_con.close()

        return res

    @staticmethod
    def get_divergent(arch_a: str, arch_b: str) -> set[str]:
        """Find packages with divergent dependencies between two architectures.

        Parameters
        ----------
        arch_a : str
            The first target architecture for comparison.
        arch_b : str
            The second target architecture for comparison.

        Returns
        -------
        set[str]
            Set containing package names with divergent dependencies.

        Note
        ----
        The release version is set to "jammy".
        """
        from depinspect.validator import db_not_exists

        res: set[str] = set()

        release = "jammy"

        db = DATABASE_DIR / "ubuntu" / f"ubuntu_{release}{DB_SUFFIX}"

        if db_not_exists(db):
            return set()

        db_con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)

        pkgs = Ubuntu.get_stored_packages()

        for pkg in pkgs:
            depends_a = database.find_dependencies(
                db_con=db_con, table="depends", arch=arch_a, name=pkg
            )
            depends_b = database.find_dependencies(
                db_con=db_con, table="depends", arch=arch_b, name=pkg
            )
            if not (depends_a.issubset(depends_b) and depends_b.issubset(depends_a)):
                res.add(pkg)

        db_con.close()

        return res
