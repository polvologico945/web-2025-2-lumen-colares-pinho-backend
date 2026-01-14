from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # pyright: ignore[reportMissingImports]
from .base import DATABASE_URL  # aponta para sqlite:///.../lumen.db

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # recomendação p/ SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
