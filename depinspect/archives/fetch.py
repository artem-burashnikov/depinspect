from pathlib import Path
from urllib import request


def pull_target_from_url(target_url: str, local_target_path: Path) -> None:
    with request.urlopen(request.Request(target_url), timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(target_url, local_target_path)


def fetch_and_save_metadata(
    data: dict[str, dict[str, dict[str, dict[str, str]]]], output_directory: Path
) -> None:
    for distribution in data.keys():
        for release in data[distribution].keys():
            for branch in data[distribution][release].keys():
                for architecture in data[distribution][release][branch].keys():
                    local_target_path = (
                        output_directory
                        / f"{distribution}_{release}_{branch}_{architecture}.xz"
                    )

                    url = data[distribution][release][branch][architecture]

                    pull_target_from_url(url, local_target_path)
