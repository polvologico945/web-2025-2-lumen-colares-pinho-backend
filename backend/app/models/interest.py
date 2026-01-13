from sqlalchemy import Column, Integer, String
from .base import Base


class Interest(Base):
    __tablename__ = "interesses"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
