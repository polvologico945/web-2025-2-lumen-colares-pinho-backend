import json
import urllib.request

def post(url, data):
    data_bytes = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode('utf-8')
            return resp.getcode(), body
    except Exception as e:
        return None, str(e)

URL = 'http://127.0.0.1:8000/auth/login'

tests = [
    {'email':'maria.barros@alu.ufc.br', 'password':'since2023'},
    {'email':'carlaevelyn@alu.ufc.br', 'password':'senha123'}
]

for t in tests:
    code, body = post(URL, t)
    print('Request:', t)
    print('Status:', code)
    print('Body:', body)
    print('---')
