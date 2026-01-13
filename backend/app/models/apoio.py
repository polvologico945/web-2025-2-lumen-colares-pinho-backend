from sqlalchemy import Column, Integer, DateTime, ForeignKey
from .base import Base


class Apoio(Base):
    __tablename__ = "apoios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
