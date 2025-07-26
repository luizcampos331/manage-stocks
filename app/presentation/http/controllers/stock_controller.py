from fastapi import APIRouter, Path
from pydantic import BaseModel

from app.application.use_cases.get_stock_details_use_case import GetStockDetailsUseCase
from app.application.use_cases.register_stock_purchase_use_case import (
    RegisterStockPurchaseUseCase,
)
from app.infra.factories.database.databse_config_factory import DatabaseConfigFactory
from app.infra.factories.gateways.stock_values_gateway_factory import (
    StockValuesGatewayFactory,
)
from app.infra.factories.gateways.stock_web_scraping_gateway_factory import (
    StockWebScrapingGatewayFactory,
)
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
    @stock_router.get("/{stock_symbol}")
    async def get_details(
        stock_symbol: str = Path(...),
    ):
        session = DatabaseConfigFactory().get_session()

        async with session:
            stock_repository = StockRepositoryFactory.make(session)
            stock_values_gateway = StockValuesGatewayFactory().make()
            stock_web_scraping_gateway = StockWebScrapingGatewayFactory().make()
            cache = CacheFactory().make()
            get_stock_details_use_case = GetStockDetailsUseCase(
                stock_repository,
                stock_values_gateway,
                stock_web_scraping_gateway,
                cache,
            )

            return await get_stock_details_use_case.execute(stock_symbol)

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
