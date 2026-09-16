"""
Configuração da conexão com o banco de dados.
Usamos SQLite (arquivo local) + SQLAlchemy como ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho do arquivo do banco SQLite (fica na raiz da pasta backend)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# check_same_thread=False é necessário só para SQLite + FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sessões do banco (cada requisição usa uma sessão)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que todos os models (tabelas) vão herdar
Base = declarative_base()


def get_db():
    """
    Dependency do FastAPI: abre uma sessão do banco,
    entrega para a rota usar, e garante que fecha no final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
