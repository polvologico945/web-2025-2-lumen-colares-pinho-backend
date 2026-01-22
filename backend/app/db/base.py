from pathlib import Path
from sqlalchemy.orm import declarative_base

Base = declarative_base()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "lumen.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
