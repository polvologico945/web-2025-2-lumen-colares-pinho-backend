from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.user_interest import (
    create_user_interest,
    get_user_interest,
    list_user_interests,
    list_user_interests_by_user,
    delete_user_interest,
)
from app.schemas.user_interest import (
    UserInterestCreate,
    UserInterestRead,
)

router = APIRouter()


@router.post("/", response_model=UserInterestRead)
def create_user_interest_endpoint(
    ui_in: UserInterestCreate, db: Session = Depends(get_db)
):
    return create_user_interest(db=db, ui_in=ui_in)


@router.get("/", response_model=List[UserInterestRead])
def list_user_interests_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_user_interests(db=db, skip=skip, limit=limit)


@router.get("/by-user/{user_id}", response_model=List[UserInterestRead])
def list_user_interests_by_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    return list_user_interests_by_user(db=db, user_id=user_id)


@router.get("/{user_interest_id}", response_model=UserInterestRead)
def get_user_interest_endpoint(
    user_interest_id: int,
    db: Session = Depends(get_db),
):
    ui = get_user_interest(db=db, user_interest_id=user_interest_id)
    if not ui:
        raise HTTPException(status_code=404, detail="Ligação não encontrada")
    return ui


@router.delete("/{user_interest_id}", status_code=204)
def delete_user_interest_endpoint(
    user_interest_id: int,
    db: Session = Depends(get_db),
):
    delete_user_interest(db=db, user_interest_id=user_interest_id)
