from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.interest import Interest
from app.schemas.interest import InterestCreate, InterestUpdate


def get_interest(db: Session, interest_id: int) -> Optional[Interest]:
    return db.query(Interest).filter(Interest.id == interest_id).first()


def list_interests(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Interest]:
    return db.query(Interest).offset(skip).limit(limit).all()


def create_interest(db: Session, interest_in: InterestCreate) -> Interest:
    db_interest = Interest(**interest_in.dict())
    db.add(db_interest)
    db.commit()
    db.refresh(db_interest)
    return db_interest


def update_interest(
    db: Session, interest_id: int, interest_in: InterestUpdate
) -> Optional[Interest]:
    db_interest = get_interest(db, interest_id)
    if not db_interest:
        return None

    data = interest_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_interest, field, value)

    db.commit()
    db.refresh(db_interest)
    return db_interest


def delete_interest(db: Session, interest_id: int) -> None:
    db.query(Interest).filter(Interest.id == interest_id).delete()
    db.commit()
