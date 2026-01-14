from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user_interest import UserInterest
from app.schemas.user_interest import UserInterestCreate


def get_user_interest(
    db: Session, user_interest_id: int
) -> Optional[UserInterest]:
    return (
        db.query(UserInterest)
        .filter(UserInterest.id == user_interest_id)
        .first()
    )


def list_user_interests(
    db: Session, skip: int = 0, limit: int = 100
) -> List[UserInterest]:
    return (
        db.query(UserInterest)
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_user_interests_by_user(
    db: Session, user_id: int
) -> List[UserInterest]:
    return db.query(UserInterest).filter(
        UserInterest.user_id == user_id
    ).all()


def create_user_interest(
    db: Session, ui_in: UserInterestCreate
) -> UserInterest:
    db_ui = UserInterest(**ui_in.dict())
    db.add(db_ui)
    db.commit()
    db.refresh(db_ui)
    return db_ui


def delete_user_interest(db: Session, user_interest_id: int) -> None:
    db.query(UserInterest).filter(
        UserInterest.id == user_interest_id
    ).delete()
    db.commit()
