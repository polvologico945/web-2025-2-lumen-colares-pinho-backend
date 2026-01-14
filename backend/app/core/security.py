from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
import hashlib
import re

SECRET_KEY = "troque-por-uma-string-bem-grande-e-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # try passlib/bcrypt first
    try:
        if pwd_context.identify(hashed_password):
            return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # fall through to sha256 check
        pass

    # fallback: if stored hash looks like a hex SHA-256, compare directly
    if isinstance(hashed_password, str) and re.fullmatch(r"[0-9a-f]{64}", hashed_password):
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest() == hashed_password

    return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
