"""
Lógica de autenticação:
- Hash de senha (nunca salvamos senha em texto puro)
- Criação e verificação de token JWT
- Dependency para proteger rotas (descobrir "quem é o usuário logado")
"""

from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
import models

# ⚠️ Em produção, essa chave deve vir de uma variável de ambiente (.env),
# nunca deixar fixa no código. Aqui está fixa só para facilitar o início do projeto.
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Diz ao FastAPI onde o cliente deve mandar usuário/senha para obter o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_senha(senha: str) -> str:
    """Transforma a senha em um hash seguro para salvar no banco."""
    return pwd_context.hash(senha)


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Compara a senha digitada com o hash salvo no banco."""
    return pwd_context.verify(senha_pura, senha_hash)


def criar_token_acesso(dados: dict, expira_em: Optional[timedelta] = None) -> str:
    """Gera um token JWT contendo os dados informados (ex: e-mail do usuário)."""
    to_encode = dados.copy()
    expira = datetime.utcnow() + (expira_em or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    """
    Dependency usada em rotas protegidas.
    Lê o token enviado pelo front, valida e retorna o usuário correspondente.
    Uso em uma rota nova: def minha_rota(usuario = Depends(obter_usuario_atual)):
    """
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credenciais_invalidas
    except JWTError:
        raise credenciais_invalidas

    usuario = db.query(models.User).filter(models.User.email == email).first()
    if usuario is None:
        raise credenciais_invalidas
    return usuario
