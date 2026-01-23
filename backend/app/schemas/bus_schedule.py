from pydantic import BaseModel

class BusScheduleBase(BaseModel):
    trip_number: int
    bus_type: str
    departure_terminal: str
    departure_campus: str
    status: str = "operando"

class BusScheduleCreate(BusScheduleBase):
    pass

class BusScheduleUpdate(BusScheduleBase):
    pass

class BusScheduleRead(BusScheduleBase):
    id: int

    class Config:
        from_attributes = True
