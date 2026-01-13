from sqlalchemy import Column, Integer, String
from .base import Base


class BusInfo(Base):
    __tablename__ = "bus_info"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=True)
    routes_text = Column(String, nullable=True)
