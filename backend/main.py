"""
Ponto de entrada da API.
Para rodar:  uvicorn main:app --reload
Documentação automática em: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import schemas
import auth
from database import engine, get_db

# Cria as tabelas no banco (se ainda não existirem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Login e Cadastro")

# Libera o front-end (rodando em outra origem/porta) para chamar essa API.
# Em produção, troque "*" pela URL real do seu front.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/cadastro", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: schemas.UserCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário no banco."""
    usuario_existente = db.query(models.User).filter(models.User.email == dados.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_usuario = models.User(
        nome=dados.nome,
        email=dados.email,
        senha_hash=auth.hash_senha(dados.senha),
        placa=dados.placa,
        modelo=dados.modelo,
        cor=dados.cor,
        vaga=dados.vaga,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autentica o usuário e devolve um token JWT.
    Obs: o OAuth2PasswordRequestForm espera os campos 'username' e 'password'
    (usamos o e-mail como 'username'). O front precisa enviar como form-data.
    """
    usuario = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not usuario or not auth.verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )

    token = auth.criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserOut)
def perfil(usuario_atual: models.User = Depends(auth.obter_usuario_atual)):
    """
    Rota protegida de exemplo: só responde se o token for válido.
    Use esse padrão (Depends(auth.obter_usuario_atual)) em toda rota nova
    que precisar exigir que o usuário esteja logado.
    """
    return usuario_atual


# 👉 Ponto de expansão: suas próximas funcionalidades (ex: vagas, tarefas, posts)
# entram aqui como novas rotas, cada uma podendo usar Depends(auth.obter_usuario_atual)
# para saber quem está logado.
