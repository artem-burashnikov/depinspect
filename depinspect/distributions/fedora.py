import logging
import sqlite3
from pathlib import Path

from depinspect.archives.extractor import (
    extract_bz2_archive,
    extract_xz_archive,
    process_archives,
)
from depinspect.archives.fetcher import fetch_and_save_metadata
from depinspect.constants import DATABASE_DIR, DB_SUFFIX, FEDORA_ARCHS
from depinspect.database import database
from depinspect.distributions.package import Package
from depinspect.files import list_files_in_directory


class Fedora(Package):
    @staticmethod
    def parse_metadata(file_path: Path, release: str) -> list["Package"]:
        return super(Fedora, Fedora).parse_metadata(file_path, release)

    @staticmethod
    def init(
        tmp_dir: Path,
        config: dict[str, dict[str, dict[str, dict[str, str]]]],
        db_suffix: str,
        output_path: Path,
    ) -> None:
        """Initialize and fetch metadata for Fedora releases.

        Parameters
        ----------
        tmp_dir : Path
            Temporary directory for fetching and extracting archives.
        config : dict[str, dict[str, dict[str, dict[str, str]]]]
            Configuration dictionary.
        db_suffix : str
            Desired file extension for the extracted databases.
        output_path : Path
            The directory where the extracted databases will be saved.
        """
        try:
            for release in config["fedora"].keys():
                logging.info("Fetching fedora archives.")
                fetch_and_save_metadata(config, "fedora", tmp_dir)

                logging.info("Extracting fedora xz archives.")
                process_archives(
                    input_dir=tmp_dir,
                    output_dir=output_path,
                    file_extension=db_suffix,
                    archive_extension=".xz",
                    extractor=extract_xz_archive,
                )

                logging.info("Extracting fedora bz2 archives.")
                process_archives(
                    input_dir=tmp_dir,
                    output_dir=output_path,
                    file_extension=db_suffix,
                    archive_extension=".bz2",
                    extractor=extract_bz2_archive,
                )
        except Exception:
            logging.exception("There was an exception trying to pull fedora database.")

    @staticmethod
    def get_all_archs() -> set[str]:
        """Get the set of all Fedora architectures."""
        return FEDORA_ARCHS

    @staticmethod
    def get_stored_packages() -> set[str]:
        """Get the set of all distinct package names stored in Fedora databases.

        Returns
        -------
        set[str]
            Set containing all distinct package names stored in Fedora databases.
        """
        res: set[str] = set()

        databases = list_files_in_directory(DATABASE_DIR / "fedora")

        for db_path in databases:
            db_con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

            for arch in Fedora.get_all_archs():
                res.update(database.find_all_distinct(db_con, arch))

            db_con.close()

        return res

    @staticmethod
    def get_dependencies(arch: str, pkg: str) -> set[str]:
        """Get the dependencies of a package for a specific architecture.

        Parameters
        ----------
        arch : str
            The target architecture for which dependencies are retrieved.
        pkg : str
            The name of the package for which dependencies are retrieved.

        Returns
        -------
        set[str]
            Set containing the dependencies of the specified package
            for the given architecture.

        Raises
        ------
        ValueError
            If the provided architecture is not supported.

        Note
        ----
        The "riscv64" architecture uses the "koji" repo, while others use "everything".
        """
        repo = "koji" if arch == "riscv64" else "everything"

        db = DATABASE_DIR / "fedora" / f"fedora_f39_{repo}_{arch}{DB_SUFFIX}"

        db_con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)

        res = database.find_dependencies(
            db_con=db_con,
            table="requires",
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
        The "riscv64" arhchitecture uses the "koji" repo, while others use "everything".
        """
        result: set[str] = set()

        repo_a = "koji" if arch_a == "riscv64" else "everything"
        repo_b = "koji" if arch_b == "riscv64" else "everything"

        db_a = DATABASE_DIR / "fedora" / f"fedora_f39_{repo_a}_{arch_a}{DB_SUFFIX}"
        db_con_a = sqlite3.connect(f"file:{db_a}?mode=ro", uri=True)

        db_b = DATABASE_DIR / "fedora" / f"fedora_f39_{repo_b}_{arch_b}{DB_SUFFIX}"
        db_con_b = sqlite3.connect(f"file:{db_b}?mode=ro", uri=True)

        pkgs = Fedora.get_stored_packages()

        for pkg in pkgs:
            depends_a = database.find_dependencies(
                db_con=db_con_a, table="requires", arch=arch_a, name=pkg
            )
            depends_b = database.find_dependencies(
                db_con=db_con_b, table="requires", arch=arch_b, name=pkg
            )
            if not (depends_a.issubset(depends_b) and depends_b.issubset(depends_a)):
                result.add(pkg)

        db_con_a.close()
        db_con_b.close()

        return result
