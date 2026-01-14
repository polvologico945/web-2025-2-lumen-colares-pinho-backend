from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserLogin, UserRead
from app.models.user import User
from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/login")
def login_endpoint(credentials: UserLogin, db: Session = Depends(get_db)):
    user: User | None = (
        db.query(User).filter(User.email == credentials.email).first()
    )
    if not user or not verify_password(credentials.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserRead.from_orm(user),
    }
