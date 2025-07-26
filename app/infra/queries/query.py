from abc import ABC, abstractmethod

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class Query(ABC):
    @abstractmethod
    async def ping(self) -> None:
        pass


class SqlalchemyQuery(Query):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def ping(self) -> None:
        await self.session.execute(text("SELECT 1"))
