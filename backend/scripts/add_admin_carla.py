import os
import sqlite3
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'db', 'lumen.db')

def sha256(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def add_admin_carla():
    db_file = os.path.abspath(DB_PATH)
    if not os.path.exists(db_file):
        print('Banco não encontrado em', db_file)
        return

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Ensure email unique; skip if already exists
    admin_email = 'carla@teste.com'
    cur.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
    if cur.fetchone():
        print('Admin Carla já existe (email:', admin_email, ')')
        conn.close()
        return

    senha_hash = sha256('senha123')
    cur.execute(
        '''INSERT INTO users (name, email, senha_hash, idade, cidade, bio, empresa, papel, curso, semestre)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ('Carla Evelyn', admin_email, senha_hash, 22, 'Quixadá', 'Estudante', 'UFC', 'admin', 'Engenharia de Software', '6')
    )
    conn.commit()
    conn.close()
    print('Admin Carla inserida (email:', admin_email, ')')

if __name__ == '__main__':
    add_admin_carla()
