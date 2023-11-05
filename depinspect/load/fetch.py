import configparser
import tempfile
from pathlib import Path
from urllib import request


def read_config(config_file_path: str) -> configparser.ConfigParser:
    """
    Read and parse a configuration file.

    Parameters:
    - config_file_path (str): The path to the configuration file.

    Returns:
    configparser.ConfigParser: A ConfigParser object containing the parsed configuration.
    """
    config = configparser.ConfigParser()
    sources_file = Path(config_file_path)
    config.read(sources_file)

    return config


def pull_target_from_URL(target_url: str, local_target_path: Path) -> None:
    """
    Fetch and save target from a given URL.

    This function downloads target data from a specified URL and saves it to a local file.
    The download uses the urllib library.

    Parameters:
    - target_url (str): The URL from which to fetch target data.
    - local_target_path (Path): The local file path to save the downloaded metadata.

    Raises:
    - urllib.error.URLError: If there is an issue with the URL or network connection.
    - urllib.error.HTTPError: If the HTTP response status is not 200 (OK).

    Note:
    The function uses an arbitrary timeout of 15.0 seconds for the request.

    Returns:
    None: The function does not return a value.
    """
    with request.urlopen(request.Request(target_url), timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(target_url, local_target_path)


def fetch_and_save_metadata_to_tmp() -> Path:
    """
    Download metadata from configured sources and save them to temporary files.

    This function reads metadata sources from the 'sources.cfg' configuration file,
    iterates through each section, and downloads metadata from the specified URLs.
    The downloaded metadata is saved to local files within a temporary folder.

    Returns:
    Path: The path to the temporary folder containing downloaded metadata.
    """
    metadata_sources = read_config("sources.cfg")

    temp_folder = Path(tempfile.mkdtemp(dir=Path.cwd(), prefix=".tmp"))

    for section in metadata_sources.sections():
        for key in metadata_sources[section]:
            file_prefix = key.split(".")[-1]
            file_name = "_packages"
            file_extension = ".xz"
            local_target_path = (
                temp_folder / f"{file_prefix}{file_name}{file_extension}"
            )

            metadata_url = metadata_sources[section][key]
            pull_target_from_URL(metadata_url, local_target_path)

    return temp_folder
