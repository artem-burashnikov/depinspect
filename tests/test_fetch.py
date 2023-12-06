from urllib import error, request

from click import echo

from depinspect.constants import PYPROJECT_TOML


# Check that all urls defined in toml configuration are reachable
def test_url_sources() -> None:
    data = PYPROJECT_TOML["tool"]["depinspect"]["archives"]

    for distribution in data.keys():
        for release in data[distribution].keys():
            for branch in data[distribution][release].keys():
                for architecture in data[distribution][release][branch].keys():
                    url = data[distribution][release][branch][architecture]

                    try:
                        with request.urlopen(
                            request.Request(url), timeout=15.0
                        ) as response:
                            # Check if the response status code is success
                            assert (
                                200 <= response.status < 300
                            ), f"Unexpected status code for {url}: {response.status}"
                    except error.URLError as e:
                        echo(f"Error accessing URL {url}: {e}")
                        assert False, f"Error accessing URL {url}: {e}"
                    except Exception as e:
                        echo(f"Unexpected error for URL {url}: {e}")
                        assert False, f"Unexpected error for URL {url}: {e}"
