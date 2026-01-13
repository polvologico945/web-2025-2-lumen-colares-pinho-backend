from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(String, nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    autor = relationship("User", back_populates="posts")
    