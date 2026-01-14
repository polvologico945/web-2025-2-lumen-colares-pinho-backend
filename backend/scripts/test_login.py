import requests

resp = requests.post(
    'http://127.0.0.1:8000/auth/login',
    json={'email': 'maria.barros@alu.ufc.br', 'password': 'since2023'},
)
print('status:', resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)
