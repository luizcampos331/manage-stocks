import os
from abc import ABC, abstractmethod
from datetime import date
from typing import TypedDict

from polygon import RESTClient


class GetStockValuesBySymbolInput(TypedDict):
    stock_symbol: str
    date: date


class StockValues(TypedDict):
    open: float
    high: float
    low: float
    close: float


class GetStockValuesBySymbolOutput(TypedDict):
    status: str
    stock_values: StockValues


class StockValuesGateway(ABC):
    @abstractmethod
    async def get_by_symbol(
        self, data: GetStockValuesBySymbolInput
    ) -> GetStockValuesBySymbolOutput:
        pass


class PolygonStockValuesGateway(StockValuesGateway):
    def __init__(self):
        self.client = RESTClient(os.getenv("STOCK_API_KEY"))

    async def get_by_symbol(
        self, data: GetStockValuesBySymbolInput
    ) -> GetStockValuesBySymbolOutput:
        result = self.client.get_daily_open_close_agg(
            ticker=data["stock_symbol"],
            date=data["date"].isoformat(),
            adjusted="true",
        )

        return {
            "status": result.status,
            "stock_values": {
                "open": result.open,
                "high": result.high,
                "low": result.low,
                "close": result.close,
            },
        }
