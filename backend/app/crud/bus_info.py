from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.bus_info import BusInfo
from app.schemas.bus_info import BusInfoCreate, BusInfoUpdate


def get_bus_info(db: Session, info_id: int) -> Optional[BusInfo]:
    return db.query(BusInfo).filter(BusInfo.id == info_id).first()


def list_bus_info(
    db: Session, skip: int = 0, limit: int = 100
) -> List[BusInfo]:
    return db.query(BusInfo).offset(skip).limit(limit).all()


def create_bus_info(
    db: Session, info_in: BusInfoCreate
) -> BusInfo:
    db_info = BusInfo(**info_in.dict())
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info


def update_bus_info(
    db: Session, info_id: int, info_in: BusInfoUpdate
) -> Optional[BusInfo]:
    db_info = get_bus_info(db, info_id)
    if not db_info:
        return None

    data = info_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_info, field, value)

    db.commit()
    db.refresh(db_info)
    return db_info


def delete_bus_info(db: Session, info_id: int) -> None:
    db.query(BusInfo).filter(BusInfo.id == info_id).delete()
    db.commit()
