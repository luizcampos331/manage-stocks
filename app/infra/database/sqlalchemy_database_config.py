import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL")
ECHO_SQL = os.getenv("DATABASE_LOGS", "false").lower() == "true"


# Criar engine apenas se DATABASE_URL estiver disponível
def get_engine():
    if DATABASE_URL:
        return create_async_engine(DATABASE_URL, echo=ECHO_SQL)
    return None


# Criar sessionmaker apenas se engine estiver disponível
def get_session_maker():
    engine = get_engine()
    if engine:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )
    return None


# Para compatibilidade com código existente
SqlalchemyDatabaseConfig = get_session_maker()


class BaseSqlalchemyDatabaseConfig(DeclarativeBase):
    pass
