from app.db.session import engine
from app.models.base import Base
from app.models.user import User
from app.models.post import Postagem

def init_db():
    Base.metadata.create_all(bind=engine)
