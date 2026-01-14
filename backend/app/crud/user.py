from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.security import hash_password

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        name=user_in.name,
        email=user_in.email,
        senha_hash=hash_password(user_in.password),
        idade=user_in.idade,
        cidade=user_in.cidade,
        bio=user_in.bio,
        empresa=user_in.empresa,
        avatar_url=user_in.avatar_url,
        papel=user_in.papel,
        curso=user_in.curso,
        semestre=user_in.semestre,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, user_id: int, user_in: UserUpdate
) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    data = user_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
