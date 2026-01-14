import sys
import os
import hashlib

# allow imports from app package
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from app.db.session import SessionLocal
from app.models.user import User


def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def main():
    db = SessionLocal()
    try:
        email = "maria.barros@alu.ufc.br"
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"Usuário já existe: id={existing.id} email={existing.email}")
            return

        senha = "since2023"
        senha_hash = sha256_hash(senha)

        user = User(
            name="Maria Barros",
            email=email,
            senha_hash=senha_hash,
            idade=23,
            cidade="Quixadá",
            curso="Engenharia de Software",
            papel="user",
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Inserido usuário: id={user.id} email={user.email} senha_hash={user.senha_hash}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
