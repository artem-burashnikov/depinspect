from depinspect.helper import get_project_root

# Asuuming config and database files are in the project root
ROOT_DIR = get_project_root()

SOURCES_FILE_NAME = "sources.cfg"
SOURCES_FILE_PATH = ROOT_DIR / SOURCES_FILE_NAME

DB_NAME = "dependencies.db"

ARCHITECTURES = ["i386", "amd64", "riscv64", "any", "all"]
