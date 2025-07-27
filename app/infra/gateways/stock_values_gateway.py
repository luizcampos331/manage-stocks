import os
from abc import ABC, abstractmethod
from datetime import date
from typing import TypedDict

from polygon import BadResponse, RESTClient

from app.infra.exceptions.infra_exception import InfraException


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
        try:
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
        except BadResponse as e:
            if "not_found" in str(e).lower():
                raise InfraException(
                    status="NOT_FOUND",
                    message=f"Data not found for stock symbol '{data['stock_symbol']}' on {data['date'].isoformat()}.",
                )

            raise RuntimeError(f"Unexpected error from Polygon API: {str(e)}")
