from typing import Any
from urllib import request

import pytest

from depinspect.constants import PYPROJECT_TOML


# Define a fixture to get the URLs from the configuration
@pytest.fixture
def urls_from_config() -> Any:
    return PYPROJECT_TOML.get("tool", {}).get("depinspect", {}).get("archives", {})


def check_url(url: str) -> None:
    try:
        with request.urlopen(request.Request(url), timeout=15.0) as response:
            # Check if the response status code is success
            assert (
                200 <= response.status < 300
            ), f"Unexpected status code for {url}: {response.status}"
    except Exception as e:
        assert False, f"Unexpected error for URL {url}: {e}"


def test_url_sources(
    urls_from_config: dict[str, dict[str, dict[str, dict[str, str]]]]
) -> None:
    for _, releases in urls_from_config.items():
        for _, branches in releases.items():
            for _, architectures in branches.items():
                for _, url in architectures.items():
                    check_url(url)
