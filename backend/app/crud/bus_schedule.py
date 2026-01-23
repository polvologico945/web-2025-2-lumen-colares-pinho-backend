from sqlalchemy.orm import Session
from app.models.bus_schedule import BusSchedule
from app.schemas.bus_schedule import BusScheduleCreate

def get_bus_schedule(db: Session, schedule_id: int):
    return db.query(BusSchedule).filter(BusSchedule.id == schedule_id).first()

def list_bus_schedules(db: Session, bus_type: str = None, skip: int = 0, limit: int = 100):
    query = db.query(BusSchedule)
    if bus_type:
        query = query.filter(BusSchedule.bus_type == bus_type)
    return query.order_by(BusSchedule.trip_number).offset(skip).limit(limit).all()

def create_bus_schedule(db: Session, schedule: BusScheduleCreate):
    db_schedule = BusSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def delete_bus_schedule(db: Session, schedule_id: int):
    db_obj = db.query(BusSchedule).filter(BusSchedule.id == schedule_id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
