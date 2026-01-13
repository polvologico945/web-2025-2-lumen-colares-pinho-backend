from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
