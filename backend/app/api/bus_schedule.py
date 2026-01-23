from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.bus_schedule import BusScheduleRead, BusScheduleCreate
from app.crud import bus_schedule as crud_schedule

router = APIRouter()

@router.get("/", response_model=List[BusScheduleRead])
def read_schedules(
    bus_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista horários de ônibus.
    Pode filtrar por bus_type ('A' ou 'B').
    """
    return crud_schedule.list_bus_schedules(db=db, bus_type=bus_type, skip=skip, limit=limit)

@router.post("/", response_model=BusScheduleRead, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule: BusScheduleCreate,
    db: Session = Depends(get_db)
):
    return crud_schedule.create_bus_schedule(db=db, schedule=schedule)

@router.get("/by-type/{bus_type}", response_model=List[BusScheduleRead])
def read_schedules_by_type(
    bus_type: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint específico para compatibilidade, se necessário.
    Retorna apenas os horários do tipo especificado.
    """
    return crud_schedule.list_bus_schedules(db=db, bus_type=bus_type)
