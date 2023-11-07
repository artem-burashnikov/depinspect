import configparser
from pathlib import Path
from urllib import request


def read_config(config_path: Path) -> configparser.ConfigParser:
    """
    Reads and parses a configuration file using the configparser module.

    Args:
    - config_path: The path to the configuration file.

    Returns:
    configparser.ConfigParser: A ConfigParser object containing the parsed configuration.
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def pull_target_from_URL(target_url: str, local_target_path: Path) -> None:
    """
    Downloads a file from a given URL and saves it to the specified local path.

    Args:
    - target_url (str): The URL of the file to be downloaded.
    - local_target_path (Path): The local path where the downloaded file will be saved.

    Raises:
    - URLError: If there is an issue with the URL.
    - HTTPError: If the HTTP request returns an error status.
    """
    with request.urlopen(request.Request(target_url), timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(target_url, local_target_path)


def fetch_and_save_metadata(config_path: Path, output_directory: Path) -> None:
    """
    Fetches metadata from multiple sources based on the configuration and saves the files to the specified output directory.

    Args:
    - config_path (Path): The path to the configuration file specifying metadata sources.
    - output_directory (Path): The directory where the downloaded metadata files will be saved.
    """
    metadata_sources = read_config(config_path)

    for section in metadata_sources.sections():
        for key in metadata_sources[section]:
            file_prefix = key.split(".")[-1]
            file_name = "packages"
            file_extension = "xz"
            local_target_path = (
                output_directory
                / f"{section}_{file_prefix}_{file_name}.{file_extension}"
            )

            metadata_url = metadata_sources[section][key]

            pull_target_from_URL(metadata_url, local_target_path)
