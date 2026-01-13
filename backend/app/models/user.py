from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    idade = Column(Integer, nullable=True)
    cidade = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    empresa = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    papel = Column(String, nullable=False, default="user")  # "user" | "admin"
    curso = Column(String, nullable=True)
    semestre = Column(String, nullable=True)


    
    posts = relationship("Postagem", back_populates="autor")
    interests = relationship("UserInterest", back_populates="user")