from depinspect.constants import ROOT_DIR

from depinspect.distributions.ubuntu import Ubuntu
from depinspect.files import list_files_in_directory

def test_ubuntu_parsing():
    # Get a list of Ubuntu package metadata files in the test_data directory
    ubuntu_packages = [file for file in list_files_in_directory(ROOT_DIR / "tests" / "test_data") if file.name == "test_ubuntu_parsing.txt"]
    
    # Deserialize the packages and store them in a dictionary
    deserialized_packages = {ubuntu_package: Ubuntu.parse_matadata(ubuntu_package) for ubuntu_package in ubuntu_packages}
    
    # Iterate over each metadata file and its corresponding list of packages
    for metadata_file, list_of_packages in deserialized_packages.items():
        with open(metadata_file, 'r') as f:
            # Read the contents of the metadata file
            metadata = f.read()

            # Iterate over each package entry and assert that it is present in the metadata
            for entry in list_of_packages:
                assert f'Package: {entry.package}\n' in metadata, f"Package {entry.package} not found in {metadata_file}"
