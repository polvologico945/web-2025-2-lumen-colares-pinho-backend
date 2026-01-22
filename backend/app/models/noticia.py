from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base


class Noticia(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    type = Column(String, nullable=False)  # "evento", "manutencao", etc.
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
