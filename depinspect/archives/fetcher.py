from pathlib import Path
from urllib import request


def pull_target_from_url(target_url: str, local_target_path: Path) -> None:
    """Pull a target from a given URL and save it to a local file.

    Parameters
    ----------
    target_url : str
        The URL of the target to be pulled.
    local_target_path : Path
        The local path where the target will be saved.

    Raises
    ------
    ValueError
        If the target URL does not start with "http".
    """
    if target_url.lower().startswith("http"):
        req = request.Request(target_url)
    else:
        raise ValueError from None

    with request.urlopen(req, timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(target_url, local_target_path)


def fetch_and_save_metadata(
    config: dict[str, dict[str, dict[str, dict[str, str]]]],
    distribution: str,
    output_directory: Path,
) -> None:
    """Fetch and save metadata for a specified distribution.

    Parameters
    ----------
    config : Dict[str, Dict[str, Dict[str, Dict[str, str]]]]
        Configuration dictionary.
    distribution : str
        The distribution for which metadata should be fetched and saved.
    output_directory : Path
        The directory where the fetched metadata will be saved.

    Returns
    -------
    None
    """
    for release, branches in config[distribution].items():
        for branch, archs in branches.items():
            for arch, url in archs.items():
                archive_ext = url.split(".")[-1]

                file_name = f"{distribution}_{release}_{branch}_{arch}.{archive_ext}"

                local_target_path = output_directory / file_name

                pull_target_from_url(url, local_target_path)
