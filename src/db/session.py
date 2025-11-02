from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

# Cria a "engine" de conexão com o banco de dados usando a URL do .env
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Cria uma fábrica de sessões configurada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)