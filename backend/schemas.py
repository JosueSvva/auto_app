"""
Schemas = formato dos dados que entram e saem da API.
Usamos Pydantic para validar automaticamente (ex: e-mail válido, campos obrigatórios).
"""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Dados esperados no CADASTRO (registro)."""
    nome: str
    email: EmailStr
    senha: str


class UserLogin(BaseModel):
    """Dados esperados no LOGIN."""
    email: EmailStr
    senha: str


class UserOut(BaseModel):
    """Dados do usuário que a API pode devolver (nunca a senha!)."""
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True  # permite converter direto do model do SQLAlchemy


class Token(BaseModel):
    """Resposta do login: o token de acesso."""
    access_token: str
    token_type: str = "bearer"


# 👉 Ponto de expansão: quando adicionar novos campos ao User (models.py),
# lembre de refletir aqui também (ex: UserUpdate, UserCreate com novos campos).
