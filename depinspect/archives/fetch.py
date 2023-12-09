from pathlib import Path
from urllib import request


def pull_target_from_url(target_url: str, local_target_path: Path) -> None:
    if target_url.lower().startswith("http"):
        req = request.Request(target_url)
    else:
        raise ValueError from None

    with request.urlopen(req, timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(target_url, local_target_path)


def fetch_and_save_metadata(
    config: dict[str, dict[str, dict[str, dict[str, str]]]],
    output_directory: Path,
) -> None:
    for distribution, releases in config.items():
        for release, branches in releases.items():
            for branch, architectures in branches.items():
                for architecture, url in architectures.items():
                    local_target_path = (
                        output_directory
                        / f"{distribution}_{release}_{branch}_{architecture}.xz"
                    )
                    pull_target_from_url(url, local_target_path)
