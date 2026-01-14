import os
import sqlite3
from app.core.security import verify_password

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'db', 'lumen.db')

def check(email, plain):
    db_file = os.path.abspath(DB_PATH)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute('SELECT senha_hash FROM users WHERE email = ?', (email,))
    row = cur.fetchone()
    conn.close()
    if not row:
        print(email, 'not found')
        return
    hashed = row[0]
    ok = verify_password(plain, hashed)
    print(email, '->', 'OK' if ok else 'FAIL')

if __name__ == '__main__':
    checks = [
        ('maria.barros@alu.ufc.br','since2023'),
        ('carlaevelyn@alu.ufc.br','senha123')
    ]
    for e,p in checks:
        check(e,p)
