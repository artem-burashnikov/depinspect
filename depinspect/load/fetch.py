import configparser
from pathlib import Path
from urllib import request


def read_config(config_path: Path) -> configparser.ConfigParser:
    """
    Read and parse configuration settings from a file.

    Parameters:
    - config_path (Path): Path to the configuration file.

    Returns:
    - configparser.ConfigParser: ConfigParser object containing the parsed configuration settings.

    Note:
    This function reads and parses configuration settings from the specified file using ConfigParser.
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def pull_target_from_URL(target_url: str, local_target_path: Path) -> None:
    """
    Download a file from a URL and save it locally.

    Parameters:
    - target_url (str): URL of the file to be downloaded.
    - local_target_path (Path): Local path where the downloaded file will be saved.

    Returns:
    - None

    Note:
    This function downloads a file from the specified URL and saves it to the local target path.
    """
    with request.urlopen(request.Request(target_url), timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(target_url, local_target_path)


def fetch_and_save_metadata(config_path: Path, output_directory: Path) -> None:
    """
    Fetch metadata from URLs specified in a configuration file and save locally.

    Parameters:
    - config_path (Path): Path to the configuration file containing metadata URLs.
    - output_directory (Path): Local directory where the downloaded metadata files will be saved.

    Returns:
    - None

    Note:
    This function reads metadata sources from the specified configuration file,
    fetches the metadata from URLs, and saves the downloaded files to the output directory.
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
