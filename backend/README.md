# Lumen — Backend (API)

## Integrantes da Dupla
- Carla Evelyn Colares Inacio — 556574 — carlaevelyn@alu.ufc.br
- Maria José Pinho Barros — 556324 — maria.barros@alu.ufc.br

## Descrição
Este repositório contém a API do projeto Lumen, responsável pela autenticação,
gestão de perfis, postagens e sistema de convites entre usuários.

O backend fornece endpoints REST que são consumidos pelo frontend em React.

## Tecnologias Utilizadas


## Como Executar o Backend
1. Clone o repositório:
https://github.com/seuusuario/web-2025-2-lumen-colares-pinho-backend

2. Instale as dependências:
npm install

3. Crie um arquivo `.env`:
DATABASE_URL=sua_string_de_conexao_postgres

4. Execute a API:
node index.js

5. A API estará disponível em:
http://localhost:8000

API Node.js com Express para rede social universitária. 
Inclui autenticação JWT, upload de imagens (5 por post, 5MB cada) e sistema de pedidos de ajuda com -> 
fluxo transacional (pendente→aceito→concluído).
Rodar: 'npm start' 'npm run dev'. Usuários teste: carlaevelyn@alu.ufc.br/senha123 e maria.barros@alu.ufc.br/since2023.
