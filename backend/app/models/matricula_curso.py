from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base


class MatriculaCurso(Base):
    __tablename__ = "matriculas_curso"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_name = Column(String, nullable=False)
    period = Column(String, nullable=False)
