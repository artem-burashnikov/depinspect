from pathlib import Path

from depinspect.distributions.package import Package


class Fedora(Package):
    @staticmethod
    def init(
        tmp_dir: Path,
        config: dict[str, dict[str, dict[str, dict[str, str]]]],
        distribution: str,
        db_suffix: str,
        output_path: Path,
    ) -> None:
        # TODO
        pass
