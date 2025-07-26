import os

from app.infra.database.sqlalchemy_database_config import SqlalchemyDatabaseConfig

implementations = {"sqlalchemy": SqlalchemyDatabaseConfig}


class DatabaseConfigFactory:
    def __init__(self):
        implementation = os.getenv("DATABASE_IMPLEMENTATION")
        if implementation not in implementations:
            raise ValueError(f"Unsupported DATABASE_IMPLEMENTATION: {implementation}")
        self._session_factory = implementations[implementation]

    def get_session(self):
        return self._session_factory()
