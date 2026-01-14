from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.apoio import (
    create_apoio,
    get_apoio,
    list_apoios,
    list_apoios_by_post,
    delete_apoio,
)
from app.schemas.apoio import ApoioCreate, ApoioRead

router = APIRouter()


@router.post("/", response_model=ApoioRead)
def create_apoio_endpoint(
    apoio_in: ApoioCreate, db: Session = Depends(get_db)
):
    return create_apoio(db=db, apoio_in=apoio_in)


@router.get("/", response_model=List[ApoioRead])
def list_apoios_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_apoios(db=db, skip=skip, limit=limit)


@router.get("/by-post/{post_id}", response_model=List[ApoioRead])
def list_apoios_by_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db),
):
    return list_apoios_by_post(db=db, post_id=post_id)


@router.get("/{apoio_id}", response_model=ApoioRead)
def get_apoio_endpoint(
    apoio_id: int,
    db: Session = Depends(get_db),
):
    apoio = get_apoio(db=db, apoio_id=apoio_id)
    if not apoio:
        raise HTTPException(status_code=404, detail="Apoio não encontrado")
    return apoio


@router.delete("/{apoio_id}", status_code=204)
def delete_apoio_endpoint(
    apoio_id: int,
    db: Session = Depends(get_db),
):
    delete_apoio(db=db, apoio_id=apoio_id)
