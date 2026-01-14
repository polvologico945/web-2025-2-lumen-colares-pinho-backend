import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import verify_password


def main():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == 'maria.barros@alu.ufc.br').first()
        if not user:
            print('Usuário não encontrado')
            return
        print('user id', user.id)
        ok = verify_password('since2023', user.senha_hash)
        print('verify_password returned', ok)
    finally:
        db.close()


if __name__ == '__main__':
    main()
