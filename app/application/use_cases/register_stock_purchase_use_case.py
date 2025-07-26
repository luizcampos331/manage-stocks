from typing import TypedDict

from app.domain.entities.stock import Stock
from app.domain.entities.stock_transaction import StockTransaction
from app.infra.repositories.stock_repository import StockRepository
from app.infra.repositories.stock_transaction_repository import (
    StockTransactionRepository,
)
from app.infra.services.cache import Cache


class RegisterStockPurchaseInput(TypedDict):
    stock_symbol: str
    amount: float


class RegisterStockPurchaseOutput(TypedDict):
    message: str


class RegisterStockPurchaseUseCase:
    def __init__(
        self,
        stock_repository: StockRepository,
        stock_transaction_repository: StockTransactionRepository,
        cache: Cache,
    ):
        self.stock_repository = stock_repository
        self.stock_transaction_repository = stock_transaction_repository
        self.cache = cache

    async def execute(
        self, data: RegisterStockPurchaseInput
    ) -> RegisterStockPurchaseOutput:
        stock = await self.stock_repository.find_by_symbol(data["stock_symbol"])

        if stock:
            stock.increment_balance(data["amount"])
            await self.stock_repository.update(stock)
        else:
            stock = Stock(stock_symbol=data["stock_symbol"], balance=data["amount"])
            await self.stock_repository.create(data=stock)

        await self.stock_transaction_repository.create(
            data=StockTransaction(
                stock_symbol=data["stock_symbol"], amount=data["amount"]
            )
        )
        await self.cache.delete(key=data["stock_symbol"])

        return {
            "message": (
                f"{data['amount']} units of stock {data['stock_symbol']} "
                "were added to your stock record"
            )
        }
