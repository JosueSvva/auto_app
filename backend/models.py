"""
Models = como as tabelas do banco de dados são estruturadas.
Aqui temos só a tabela de usuários (base para login/cadastro).
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)  # nunca salvar senha em texto puro
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # 👉 Ponto de expansão: aqui você pode adicionar novos campos
    # conforme for criando funcionalidades novas (ex: telefone, foto, cargo, etc.)
