from fastapi import APIRouter, Path
from pydantic import BaseModel

from app.application.use_cases.register_stock_purchase_use_case import (
    RegisterStockPurchaseUseCase,
)
from app.infra.factories.database.databse_config_factory import DatabaseConfigFactory
from app.infra.factories.repositories.stock_repository_factory import (
    StockRepositoryFactory,
)
from app.infra.factories.repositories.stock_transaction_repository_factory import (
    StockTransactionRepositoryFactory,
)
from app.infra.factories.services.cache_factory import CacheFactory

stock_router = APIRouter(prefix="/stock")


class RegisterStockPurchaseRequest(BaseModel):
    amount: float


class StockController:
    @stock_router.post("/{stock_symbol}")
    async def register_purchase(
        stock_symbol: str = Path(...),
        request: RegisterStockPurchaseRequest = ...,
    ):
        session = DatabaseConfigFactory().get_session()

        async with session.begin():
            stock_repository = StockRepositoryFactory.make(session)
            stock_transaction_repository = StockTransactionRepositoryFactory.make(
                session
            )
            cache = CacheFactory().make()
            register_stock_purchase_use_case = RegisterStockPurchaseUseCase(
                stock_repository, stock_transaction_repository, cache
            )

            return await register_stock_purchase_use_case.execute(
                {"stock_symbol": stock_symbol, "amount": request.amount}
            )
