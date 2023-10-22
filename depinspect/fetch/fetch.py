from pathlib import Path
from urllib import request
import time

# url = "http://ports.ubuntu.com/dists/jammy/main/binary-riscv64/Packages.xz"
# target_path = Path.joinpath(Path(__file__).parent, "riscv64Packages.xz")


def fetch_packages_metadata(metadata_url: str, local_target_path: Path):
    # https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
    # NOTE: Transfer-Encoding: chunked (streaming) will be auto-selected
    with request.urlopen(request.Request(metadata_url), timeout=15.0) as response:
        if response.status == 200:
            request.urlretrieve(metadata_url, local_target_path)
