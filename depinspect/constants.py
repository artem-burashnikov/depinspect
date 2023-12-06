from depinspect.helper import get_project_root, parse_pyproject

ROOT_DIR = get_project_root()

PYPROJECT_TOML = parse_pyproject(ROOT_DIR / "pyproject.toml")

DB_SUFFIX = "_dependencies.db"

DISTRIBUTIONS = ["ubuntu", "fedora"]

ARCHITECTURES = ["i386", "amd64", "riscv64", "any", "all"]
