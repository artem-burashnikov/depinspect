from depinspect.helper import get_project_root, parse_pyproject

ROOT_DIR = get_project_root()

PYPROJECT_TOML = parse_pyproject(ROOT_DIR / "pyproject.toml")

DATABASE_DIR = ROOT_DIR / "depinspect" / "database"

DB_SUFFIX = ".sqlite"

DISTRIBUTIONS = ["ubuntu", "fedora"]

UBUNTU_ARCHS = ["i386", "amd64", "riscv64", "any", "all"]

FEDORA_ARCHS = ["i686", "noarch", "x86_64"]

ARCHITECTURES = [*UBUNTU_ARCHS, *FEDORA_ARCHS]
