from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.noticia import Noticia
from app.schemas.noticia import NoticiaCreate, NoticiaUpdate


def get_noticia(db: Session, noticia_id: int) -> Optional[Noticia]:
    return db.query(Noticia).filter(Noticia.id == noticia_id).first()


def list_noticias(db: Session, skip: int = 0, limit: int = 100) -> List[Noticia]:
    return (
        db.query(Noticia)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_noticia(db: Session, noticia_in: NoticiaCreate) -> Noticia:
    db_noticia = Noticia(**noticia_in.dict())
    db.add(db_noticia)
    db.commit()
    db.refresh(db_noticia)
    return db_noticia


def update_noticia(
    db: Session, noticia_id: int, noticia_in: NoticiaUpdate
) -> Optional[Noticia]:
    db_noticia = get_noticia(db, noticia_id)
    if not db_noticia:
        return None

    data = noticia_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_noticia, field, value)

    db.commit()
    db.refresh(db_noticia)
    return db_noticia


def delete_noticia(db: Session, noticia_id: int) -> None:
    db.query(Noticia).filter(Noticia.id == noticia_id).delete()
    db.commit()
