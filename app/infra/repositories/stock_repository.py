from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.stock import Stock
from app.infra.repositories.models.sqlalchemy_stock_model import StockModel


class StockRepository(ABC):
    @abstractmethod
    async def find_by_symbol(self, stock_symbol: str) -> Optional[Stock]:
        pass

    @abstractmethod
    async def create(self, data: Stock) -> None:
        pass

    @abstractmethod
    async def update(self, data: Stock) -> None:
        pass


class SqlalchemyStockRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_symbol(self, stock_symbol: str) -> Stock | None:
        result = await self.session.execute(
            select(StockModel).where(StockModel.stock_symbol == stock_symbol)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        return Stock(
            id=model.id,
            stock_symbol=model.stock_symbol,
            balance=model.balance,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create(self, data: Stock) -> None:
        model = StockModel(
            id=data.id,
            stock_symbol=data.stock_symbol,
            balance=data.balance,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
        self.session.add(model)

    async def update(self, data: Stock) -> None:
        result = await self.session.execute(
            select(StockModel).where(StockModel.stock_symbol == data.stock_symbol)
        )
        model = result.scalar_one_or_none()
        if model:
            model.balance = data.balance
