from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.apoio import Apoio
from app.schemas.apoio import ApoioCreate


def get_apoio(db: Session, apoio_id: int) -> Optional[Apoio]:
    return db.query(Apoio).filter(Apoio.id == apoio_id).first()


def list_apoios(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Apoio]:
    return db.query(Apoio).offset(skip).limit(limit).all()


def list_apoios_by_post(
    db: Session, post_id: int
) -> List[Apoio]:
    return db.query(Apoio).filter(Apoio.post_id == post_id).all()


def create_apoio(db: Session, apoio_in: ApoioCreate) -> Apoio:
    db_apoio = Apoio(
        user_id=apoio_in.user_id,
        post_id=apoio_in.post_id,
        created_at=datetime.utcnow(),
    )
    db.add(db_apoio)
    db.commit()
    db.refresh(db_apoio)
    return db_apoio


def delete_apoio(db: Session, apoio_id: int) -> None:
    db.query(Apoio).filter(Apoio.id == apoio_id).delete()
    db.commit()
