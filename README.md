# Estrutura Base — Login e Cadastro

Base pronta pra você ir adicionando funcionalidades no back e no front.

## Estrutura

```
auth-app/
├── backend/
│   ├── main.py         # rotas da API (cadastro, login, /me)
│   ├── models.py       # tabela User (banco de dados)
│   ├── schemas.py      # formatos de entrada/saída (validação)
│   ├── auth.py         # hash de senha, JWT, proteção de rotas
│   ├── database.py     # conexão com o SQLite
│   └── requirements.txt
└── frontend/
    ├── index.html       # tela de login
    ├── cadastro.html    # tela de cadastro
    ├── painel.html       # tela protegida (exemplo pós-login)
    ├── style.css
    └── script.js        # chamadas à API
```

## Como rodar o backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

A API sobe em `http://127.0.0.1:8000`. Docs automáticas em `http://127.0.0.1:8000/docs`.

## Como rodar o frontend

É HTML puro — basta abrir `frontend/index.html` no navegador, ou servir com uma
extensão tipo "Live Server" no VS Code. Se preferir via terminal:

```bash
cd frontend
python -m http.server 5500
```

## O que já funciona

- Cadastro de usuário (`POST /cadastro`) com senha "hasheada" (nunca salva em texto puro)
- Login (`POST /login`) que devolve um token JWT
- Rota protegida de exemplo (`GET /me`) que só responde com token válido
- Frontend com as 3 telas ligadas na API (login, cadastro, painel)

## Onde adicionar suas próximas funcionalidades

- **Backend**: crie novas rotas em `main.py` (ou em arquivos novos, tipo `rotas_vagas.py`).
  Para exigir login, use `Depends(auth.obter_usuario_atual)` como parâmetro da rota —
  tem um exemplo pronto na rota `/me`.
- **Modelos novos** (ex: tabela de Vagas): siga o padrão de `models.py`.
- **Frontend**: siga o padrão de `script.js` — toda chamada autenticada manda o
  header `Authorization: Bearer <token>`, que fica salvo no `localStorage`.

## Observação de segurança

A `SECRET_KEY` em `auth.py` está fixa só para facilitar o começo do projeto.
Antes de ir pra produção (ou subir pro GitHub público), troque por uma variável
de ambiente (`.env`) e nunca versione a chave real.
