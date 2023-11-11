import configparser
from pathlib import Path
from urllib import request


def read_config(config_path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def pull_target_from_URL(target_url: str, local_target_path: Path) -> None:
    with request.urlopen(request.Request(target_url), timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(target_url, local_target_path)


def fetch_and_save_metadata(config_path: Path, output_directory: Path) -> None:
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
