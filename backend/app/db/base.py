from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # pasta app
DB_PATH = BASE_DIR / "db" / "lumen.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
