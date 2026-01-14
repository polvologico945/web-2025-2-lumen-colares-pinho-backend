import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'db', 'lumen.db')

def list_users():
    db_file = os.path.abspath(DB_PATH)
    if not os.path.exists(db_file):
        print('Banco não encontrado em', db_file)
        return
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, papel, idade, cidade FROM users")
    rows = cur.fetchall()
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    conn.close()

if __name__ == '__main__':
    list_users()
