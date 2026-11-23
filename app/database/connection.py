from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Endereço do banco de dados
DATABASE_URL = "sqlite:///./raizes.db"

# Cria a conexão com o banco
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Cria as sessões para acessar o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe base para nossos modelos
class Base(DeclarativeBase):
    pass
