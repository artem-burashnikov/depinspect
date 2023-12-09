from pathlib import Path

import pytest

from depinspect.archives.extract import extract_xz_archive, process_archives
from depinspect.archives.fetch import fetch_and_save_metadata
from depinspect.database import database
from depinspect.distributions.loader import deserialize_metadata


@pytest.fixture
def data() -> dict[str, dict[str, dict[str, dict[str, str]]]]:
    return {
        "ubuntu": {
            "jammy": {
                "main": {
                    "i386": "http://archive.ubuntu.com"
                    "/ubuntu/dists/jammy/main"
                    "/binary-i386/Packages.xz"
                }
            }
        }
    }


def test_initialize_from_archives(
    tmp_path: Path, data: dict[str, dict[str, dict[str, dict[str, str]]]]
) -> None:
    fetch_and_save_metadata(data, "ubuntu", tmp_path)
    process_archives(tmp_path, tmp_path, ".txt", ".xz", extract_xz_archive)
    db_path = database.init("ubuntu_test.sqlite", tmp_path)
    deserialize_metadata(tmp_path, db_path, "ubuntu", "jammy")

    assert db_path.is_file(), "Database file is not created"
    assert db_path.suffix == ".sqlite", "Unexpected database file extension"
