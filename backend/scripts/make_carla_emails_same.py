import os
import shutil
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'db', 'lumen.db')

def backup(db_file):
    bak = db_file + '.bak'
    shutil.copy2(db_file, bak)
    print('Backup criado em', bak)

def recreate_table_without_unique(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys=off')
    conn.commit()

    # create new table without UNIQUE on email
    cur.executescript("""
    BEGIN TRANSACTION;
    CREATE TABLE users_new (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      email TEXT NOT NULL,
      senha_hash TEXT NOT NULL,
      idade INTEGER,
      cidade TEXT,
      bio TEXT,
      empresa TEXT,
      avatar_url TEXT,
      papel TEXT NOT NULL DEFAULT 'user',
      curso TEXT,
      semestre TEXT
    );
    INSERT INTO users_new (id, name, email, senha_hash, idade, cidade, bio, empresa, avatar_url, papel, curso, semestre)
      SELECT id, name, email, senha_hash, idade, cidade, bio, empresa, avatar_url, papel, curso, semestre FROM users;
    DROP TABLE users;
    ALTER TABLE users_new RENAME TO users;
    COMMIT;
    """)

    cur.execute('PRAGMA foreign_keys=on')
    conn.commit()
    conn.close()
    print('Tabela `users` recriada sem UNIQUE no email')

def set_carla_email(db_file, email):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("UPDATE users SET email = ? WHERE name LIKE 'Carla%';", (email,))
    conn.commit()
    affected = cur.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,)).fetchone()[0]
    conn.close()
    print(f'Atualizado email das Carlas para {email} — registros com esse email: {affected}')

if __name__ == '__main__':
    db_file = os.path.abspath(DB_PATH)
    if not os.path.exists(db_file):
        print('Banco não encontrado em', db_file)
        raise SystemExit(1)
    backup(db_file)
    recreate_table_without_unique(db_file)
    set_carla_email(db_file, 'carlaevelyn@alu.ufc.br')
