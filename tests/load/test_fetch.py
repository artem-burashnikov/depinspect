from urllib import error, request

from depinspect.definitions import SOURCES_FILE_PATH
from depinspect.load.fetch import read_config


# Check that all urls defined in sources.cfg are reachable
def test_URL_sources() -> None:
    metadata_sources = read_config(SOURCES_FILE_PATH)

    for section in metadata_sources.sections():
        for key in metadata_sources[section]:
            url = metadata_sources[section][key]

            try:
                with request.urlopen(request.Request(url), timeout=15.0) as response:
                    # Check if the response status code is in the range of 2xx (success)
                    assert (
                        200 <= response.status < 300
                    ), f"Unexpected status code for URL {url}: {response.status}"
            except error.URLError as e:
                print(f"Error accessing URL {url}: {e}")
                assert False, f"Error accessing URL {url}: {e}"
            except Exception as e:
                print(f"Unexpected error for URL {url}: {e}")
                assert False, f"Unexpected error for URL {url}: {e}"
