from depinspect.helper import get_project_root, parse_pyproject

ROOT_DIR = get_project_root()

PYPROJECT_TOML = parse_pyproject(ROOT_DIR / "pyproject.toml")

DATABASE_DIR = ROOT_DIR / "depinspect" / "database"

DB_SUFFIX = "_dependencies.sqlite"

DISTRIBUTIONS = ["ubuntu", "fedora"]

ARCHITECTURES = ["i386", "amd64", "riscv64", "any", "all"]
