from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.user import (
    create_user,
    get_user,
    get_user_by_email,
    list_users,
    update_user,
    delete_user,
)
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User
router = APIRouter()

#Uso: criar novos usuários., listar usuários, obter detalhes de um usuário específico,
# atualizar informações do usuário e excluir usuários.
@router.post("/", response_model=UserRead)
def create_user_endpoint(
    user_in: UserCreate, db: Session = Depends(get_db)
):
    # bloqueia e-mail duplicado (já tinha)
    existing = get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    # garante só 1 admin
    if user_in.papel == "admin":
        existing_admin = (
            db.query(User).filter(User.papel == "admin").first()
        )
        if existing_admin:
            raise HTTPException(
                status_code=400,
                detail="Já existe um administrador cadastrado",
            )

    return create_user(db=db, user_in=user_in)


@router.get("/", response_model=List[UserRead])
def list_users_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_users(db=db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user_endpoint(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
):
    user = update_user(db=db, user_id=user_id, user_in=user_in)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    delete_user(db=db, user_id=user_id)
