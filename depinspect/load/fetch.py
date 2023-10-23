# Python 3.12 has built-in tomllib for parsing toml files.
# Update python version?
import configparser
from pathlib import Path
from urllib import request


def read_config(config_file_path: str) -> configparser.ConfigParser:
    """
    Read and parse a configuration file.

    This function takes the path to a configuration file, reads its contents, and
    parses it using the `configparser` module.

    Parameters:
    - config_file_path (str): The path to the configuration file.

    Returns:
    configparser.ConfigParser: A ConfigParser object containing the parsed configuration.
    """
    config = configparser.ConfigParser()
    sources_file = Path(config_file_path)
    config.read(sources_file)

    return config


def fetch_packages_metadata(metadata_url: str, local_target_path: Path) -> None:
    """
    Fetch and save metadata from a given URL.

    This function downloads metadata from a specified URL and saves it to a local file.
    The download uses the urllib library, and it automatically handles chunked (streaming)
    transfer encoding.

    Parameters:
    - metadata_url (str): The URL from which to fetch metadata.
    - local_target_path (Path): The local file path to save the downloaded metadata.

    Raises:
    - urllib.error.URLError: If there is an issue with the URL or network connection.
    - urllib.error.HTTPError: If the HTTP response status is not 200 (OK).

    Note:
    The function uses an arbitrary timeout of 15.0 seconds for the request.

    Returns:
    None: The function does not return a value.
    """
    with request.urlopen(request.Request(metadata_url), timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(metadata_url, local_target_path)


def create_temp_folder() -> Path:
    """
    Create a temporary folder in the project root.

    Returns:
    Path: Path to the created temporary folder.
    """
    temp_folder = Path.joinpath(Path.cwd(), ".temp")

    if not temp_folder.exists():
        temp_folder.mkdir()

    return temp_folder


def main() -> None:
    """
    The main entry point of the script.

    This function reads metadata sources from the 'sources.toml' configuration file,
    iterates through each section, and downloads metadata from the specified URLs,
    saving them to local files.

    Returns:
    None
    """
    metadata_sources = read_config("sources.cfg")

    # Create a temporary folder
    temp_folder = create_temp_folder()

    for section in metadata_sources.sections():
        for count, key in enumerate(metadata_sources[section]):
            # Construct file paths and extract metadata URL
            file_prefix = str(count)
            file_name = "_Packages"
            file_extension = ".xz"
            archive = ("").join([file_prefix, file_name, file_extension])

            local_target_path = Path.joinpath(temp_folder, archive)
            metadata_url = metadata_sources[section][key]
            fetch_packages_metadata(metadata_url, local_target_path)


if __name__ == "__main__":
    main()
