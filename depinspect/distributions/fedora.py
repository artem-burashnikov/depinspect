from pathlib import Path

from depinspect.distributions.package import Package


class Fedora(Package):
    @staticmethod
    def init(
        config: dict[str, dict[str, dict[str, dict[str, str]]]],
        db_suffix: str,
        output_path: Path,
    ) -> None:
        # TODO
        pass
