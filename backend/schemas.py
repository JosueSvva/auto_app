"""
Schemas = formato dos dados que entram e saem da API.
Usamos Pydantic para validar automaticamente (ex: e-mail válido, campos obrigatórios).
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserCreate(BaseModel):
    """Dados esperados no CADASTRO (registro)."""
    nome: str = Field(max_length=100)
    email: EmailStr
    senha: str = Field(max_length=60)

    placa: str = Field(
        min_length=7,
        max_length=7,
        pattern=r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$"
    )

    modelo: str = Field(max_length=50)
    cor: str = Field(max_length=30)

    vaga: Literal["A01", "A02", "A03", "A04", "A05"]


class UserLogin(BaseModel):
    """Dados esperados no LOGIN."""
    email: EmailStr
    senha: str


class UserOut(BaseModel):
    """Dados do usuário que a API pode devolver (nunca a senha!)."""
    id: int
    nome: str
    email: EmailStr
    placa: str
    modelo: str
    cor: str
    vaga: str 

    class Config:
        from_attributes = True  # permite converter direto do model do SQLAlchemy


class Token(BaseModel):
    """Resposta do login: o token de acesso."""
    access_token: str
    token_type: str = "bearer"


# 👉 Ponto de expansão: quando adicionar novos campos ao User (models.py),
# lembre de refletir aqui também (ex: UserUpdate, UserCreate com novos campos).
