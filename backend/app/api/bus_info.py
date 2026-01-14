from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.bus_info import (
    create_bus_info,
    get_bus_info,
    list_bus_info,
    update_bus_info,
    delete_bus_info,
)
from app.schemas.bus_info import (
    BusInfoCreate,
    BusInfoRead,
    BusInfoUpdate,
)

router = APIRouter()


@router.post("/", response_model=BusInfoRead)
def create_bus_info_endpoint(
    info_in: BusInfoCreate, db: Session = Depends(get_db)
):
    return create_bus_info(db=db, info_in=info_in)


@router.get("/", response_model=List[BusInfoRead])
def list_bus_info_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_bus_info(db=db, skip=skip, limit=limit)


@router.get("/{info_id}", response_model=BusInfoRead)
def get_bus_info_endpoint(
    info_id: int,
    db: Session = Depends(get_db),
):
    info = get_bus_info(db=db, info_id=info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    return info


@router.put("/{info_id}", response_model=BusInfoRead)
def update_bus_info_endpoint(
    info_id: int,
    info_in: BusInfoUpdate,
    db: Session = Depends(get_db),
):
    info = update_bus_info(db=db, info_id=info_id, info_in=info_in)
    if not info:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    return info


@router.delete("/{info_id}", status_code=204)
def delete_bus_info_endpoint(
    info_id: int,
    db: Session = Depends(get_db),
):
    delete_bus_info(db=db, info_id=info_id)
