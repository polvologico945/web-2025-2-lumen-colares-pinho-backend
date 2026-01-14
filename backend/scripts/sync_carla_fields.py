import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'db', 'lumen.db')

def sync_carla():
    db_file = os.path.abspath(DB_PATH)
    if not os.path.exists(db_file):
        print('Banco não encontrado em', db_file)
        return

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Find admin Carla
    cur.execute("SELECT id, name, senha_hash, idade, cidade, bio, empresa, curso, semestre FROM users WHERE papel='admin' AND name LIKE 'Carla%'")
    admin = cur.fetchone()
    if not admin:
        print('Registro admin da Carla não encontrado')
        conn.close()
        return

    # Find user Carla (exclude admin email)
    cur.execute("SELECT id, email FROM users WHERE papel='user' AND name LIKE 'Carla%'")
    user_rows = cur.fetchall()
    if not user_rows:
        print('Registro user da Carla não encontrado')
        conn.close()
        return

    admin_id, admin_name, senha_hash, idade, cidade, bio, empresa, curso, semestre = admin

    for user_row in user_rows:
        user_id = user_row[0]
        cur.execute(
            '''UPDATE users SET name=?, senha_hash=?, idade=?, cidade=?, bio=?, empresa=?, curso=?, semestre=? WHERE id=?''',
            (admin_name, senha_hash, idade, cidade, bio, empresa, curso, semestre, user_id)
        )
        print(f'Sincronizado campos para user id={user_id}')

    conn.commit()
    conn.close()
    print('Sincronização concluída')

if __name__ == '__main__':
    sync_carla()
