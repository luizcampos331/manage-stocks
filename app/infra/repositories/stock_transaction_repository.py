from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.stock_transaction import StockTransaction
from app.infra.repositories.models.sqlalchemy_transaction_stock_model import (
    StockTransactionModel,
)


class StockTransactionRepository(ABC):
    @abstractmethod
    async def create(self, data: StockTransaction) -> None:
        pass


class SqlalchemyStockTransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: StockTransaction) -> None:
        model = StockTransactionModel(
            id=data.id,
            stock_symbol=data.stock_symbol,
            amount=data.amount,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
        self.session.add(model)
