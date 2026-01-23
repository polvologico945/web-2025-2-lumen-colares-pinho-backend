from sqlalchemy import Column, Integer, String, Time
from app.db.base import Base

class BusSchedule(Base):
    __tablename__ = "bus_schedules"

    id = Column(Integer, primary_key=True, index=True)
    trip_number = Column(Integer, nullable=False)  # Número da viagem
    bus_type = Column(String, nullable=False)  # "A" ou "B"
    departure_terminal = Column(String, nullable=False)  # Horário saída rodoviária (ex: "07h10")
    departure_campus = Column(String, nullable=False)  # Horário saída campus (ex: "07h25")
    status = Column(String, default="operando")  # operando, cancelado, etc
