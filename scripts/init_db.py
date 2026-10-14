import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from core.db import init_db
from core.config import DB_PATH

init_db()
print(f"Database ready: {DB_PATH}")
