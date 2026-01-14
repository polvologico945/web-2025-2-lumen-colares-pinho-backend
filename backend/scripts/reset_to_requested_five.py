import os
import sqlite3
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'db', 'lumen.db')

def sha256(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

users = [
    # Carla as admin (original admin email)
    {
        'name': 'Carla Evelyn',
        'email': 'carla@teste.com',
        'password': 'senha123',
        'idade': 22,
        'cidade': 'Quixadá',
        'bio': 'Estudante',
        'empresa': 'UFC',
        'papel': 'admin',
        'curso': 'Engenharia de Software',
        'semestre': '6'
    },
    # Seu usuário (Maria)
    {
        'name': 'Maria Barros',
        'email': 'maria.barros@alu.ufc.br',
        'password': 'since2023',
        'idade': 23,
        'cidade': 'Quixadá',
        'bio': '',
        'empresa': '',
        'papel': 'user',
        'curso': 'Engenharia de Software',
        'semestre': '8'
    },
    # Carla also as user
    {
        'name': 'Carla Evelyn',
        'email': 'carlaevelyn@alu.ufc.br',
        'password': 'senha123',
        'idade': 22,
        'cidade': 'Quixadá',
        'bio': 'Estudante',
        'empresa': 'UFC',
        'papel': 'user',
        'curso': 'Engenharia de Software',
        'semestre': '6'
    },
    # Robson (requested)
    {
        'name': 'Francisco Robson Queiroz Mendes',
        'email': 'robsonqueirozmendes@gmail.com',
        'password': 'password123',
        'idade': 23,
        'cidade': 'Quixadá',
        'bio': 'Jovem dedicado e conservador, gosta de tecnologia e trabalha a 2 anos como desenvolvedor de software',
        'empresa': 'Great',
        'papel': 'user',
        'curso': 'Engenharia de software',
        'semestre': '8'
    },
    # Fifth user (neutral placeholder)
    {
        'name': 'Pedro Nascimento',
        'email': 'pedro.nascimento@teste.com',
        'password': 'pedropass',
        'idade': 26,
        'cidade': 'Fortaleza',
        'bio': 'Analista',
        'empresa': 'Empresa Y',
        'papel': 'user',
        'curso': '',
        'semestre': ''
    }
]

def reset_and_insert():
    db_file = os.path.abspath(DB_PATH)
    if not os.path.exists(db_file):
        print('Banco não encontrado em', db_file)
        return

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Delete existing users
    cur.execute('DELETE FROM users')
    try:
        cur.execute("DELETE FROM sqlite_sequence WHERE name='users'")
    except Exception:
        pass

    for u in users:
        senha_hash = sha256(u['password'])
        cur.execute(
            '''INSERT INTO users (name, email, senha_hash, idade, cidade, bio, empresa, papel, curso, semestre)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (u['name'], u['email'], senha_hash, u['idade'], u['cidade'], u['bio'], u['empresa'], u['papel'], u['curso'], u['semestre'])
        )
        print('Inserido:', u['email'], '->', u['papel'])

    conn.commit()
    conn.close()
    print('Reset concluído: agora há', len(users), 'usuários.')

if __name__ == '__main__':
    reset_and_insert()
