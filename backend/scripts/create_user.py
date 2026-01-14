import sys
import os

# ensure backend project root is on sys.path so `app` package imports work
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.crud.user import create_user, get_user_by_email


def main():
    db = SessionLocal()
    try:
        email = "maria.barros@alu.ufc.br"
        existing = get_user_by_email(db, email)
        if existing:
            print(f"Usuário já existe: id={existing.id} email={existing.email}")
            return

        user_in = UserCreate(
            name="Maria Barros",
            email=email,
            password="abc",
            idade=23,
            cidade="Quixadá",
            curso="Engenharia de Software",
        )

        user = create_user(db, user_in)
        print(f"Criado usuário: id={user.id} email={user.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
