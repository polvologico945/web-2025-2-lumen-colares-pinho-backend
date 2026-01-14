from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.interest import (
    create_interest,
    get_interest,
    list_interests,
    update_interest,
    delete_interest,
)
from app.schemas.interest import (
    InterestCreate,
    InterestRead,
    InterestUpdate,
)

router = APIRouter()


@router.post("/", response_model=InterestRead)
def create_interest_endpoint(
    interest_in: InterestCreate, db: Session = Depends(get_db)
):
    return create_interest(db=db, interest_in=interest_in)


@router.get("/", response_model=List[InterestRead])
def list_interests_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_interests(db=db, skip=skip, limit=limit)


@router.get("/{interest_id}", response_model=InterestRead)
def get_interest_endpoint(
    interest_id: int,
    db: Session = Depends(get_db),
):
    interest = get_interest(db=db, interest_id=interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    return interest


@router.put("/{interest_id}", response_model=InterestRead)
def update_interest_endpoint(
    interest_id: int,
    interest_in: InterestUpdate,
    db: Session = Depends(get_db),
):
    interest = update_interest(
        db=db, interest_id=interest_id, interest_in=interest_in
    )
    if not interest:
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    return interest


@router.delete("/{interest_id}", status_code=204)
def delete_interest_endpoint(
    interest_id: int,
    db: Session = Depends(get_db),
):
    delete_interest(db=db, interest_id=interest_id)
