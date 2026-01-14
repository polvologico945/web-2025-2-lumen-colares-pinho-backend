from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.noticia import (
    create_noticia,
    get_noticia,
    list_noticias,
    update_noticia,
    delete_noticia,
)
from app.schemas.noticia import (
    NoticiaCreate,
    NoticiaRead,
    NoticiaUpdate,
)

router = APIRouter()


@router.post("/", response_model=NoticiaRead)
def create_noticia_endpoint(
    noticia_in: NoticiaCreate, db: Session = Depends(get_db)
):
    return create_noticia(db=db, noticia_in=noticia_in)


@router.get("/", response_model=List[NoticiaRead])
def list_noticias_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_noticias(db=db, skip=skip, limit=limit)


@router.get("/{noticia_id}", response_model=NoticiaRead)
def get_noticia_endpoint(
    noticia_id: int,
    db: Session = Depends(get_db),
):
    noticia = get_noticia(db=db, noticia_id=noticia_id)
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return noticia


@router.put("/{noticia_id}", response_model=NoticiaRead)
def update_noticia_endpoint(
    noticia_id: int,
    noticia_in: NoticiaUpdate,
    db: Session = Depends(get_db),
):
    noticia = update_noticia(db=db, noticia_id=noticia_id, noticia_in=noticia_in)
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return noticia


@router.delete("/{noticia_id}", status_code=204)
def delete_noticia_endpoint(
    noticia_id: int,
    db: Session = Depends(get_db),
):
    delete_noticia(db=db, noticia_id=noticia_id)
