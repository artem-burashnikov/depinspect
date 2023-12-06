from pathlib import Path

import pytest

from depinspect import database
from depinspect.archives.extract import process_archives
from depinspect.archives.fetch import fetch_and_save_metadata
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
    fetch_and_save_metadata(data, tmp_path)
    process_archives(tmp_path)
    db_path = database.new("ubuntu_test.db", tmp_path)
    deserialize_metadata(tmp_path, db_path, "ubuntu")

    assert db_path.is_file(), "Database file is not created"
    assert db_path.suffix == ".db", "Unexpected database file extension"
