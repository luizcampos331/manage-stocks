import os
from typing import Any

from app.infra.queries.query import SqlalchemyQuery

implementations = {
    "sqlalchemy": SqlalchemyQuery,
}


class QueryFactory:
    @staticmethod
    def make(session: Any):
        implementation = os.getenv("DATABASE_IMPLEMENTATION")
        if implementation not in implementations:
            raise ValueError(f"Unsupported DATABASE_IMPLEMENTATION: {implementation}")

        return implementations[implementation](session)
