import json
from datetime import date, timedelta
from typing import List, TypedDict

from app.infra.gateways.stock_values_gateway import StockValues, StockValuesGateway
from app.infra.gateways.stock_web_scraping_gateway import (
    StockCompetitors,
    StockPerformanceData,
    StockWebScrapingGateway,
)
from app.infra.repositories.stock_repository import StockRepository
from app.infra.services.cache import Cache


class GetStockDetailsOutput(TypedDict):
    status: str
    purchased_amount: float
    purchased_status: str
    request_data: date
    company_code: str
    company_name: str
    stock_values: StockValues
    performance_data: StockPerformanceData
    competitors: List[StockCompetitors]


class GetStockDetailsUseCase:
    def __init__(
        self,
        stock_repository: StockRepository,
        stock_values_gateway: StockValuesGateway,
        stock_web_scraping_gateway: StockWebScrapingGateway,
        cache: Cache,
    ):
        self.stock_repository = stock_repository
        self.stock_values_gateway = stock_values_gateway
        self.stock_web_scraping_gateway = stock_web_scraping_gateway
        self.cache = cache

    async def execute(self, stock_symbol: str) -> GetStockDetailsOutput:
        stock_cached = await self.cache.get(key=stock_symbol)

        if stock_cached:
            return json.loads(stock_cached)

        stock = await self.stock_repository.find_by_symbol(stock_symbol)
        stock_values = await self.stock_values_gateway.get_by_symbol(
            data={
                "date": date.today() - timedelta(days=1),
                "stock_symbol": stock_symbol,
            }
        )
        stock_web_scraping = await self.stock_web_scraping_gateway.scraping_by_symbol(
            stock_symbol
        )

        stock_cached = {
            "status": stock_values["status"],
            "purchased_amount": stock.balance if stock else 0,
            "purchased_status": "purchased" if stock else "not_purchased",
            "request_data": date.today() - timedelta(days=1),
            "company_code": stock_symbol,
            "company_name": stock_web_scraping["company_name"],
            "stock_values": stock_values["stock_values"],
            "performance_data": stock_web_scraping["performance_data"],
            "competitors": stock_web_scraping["competitors"],
        }

        await self.cache.set(
            data={
                "key": stock_symbol,
                "value": json.dumps(stock_cached, default=str),
                "ttl": 900,
            }
        )

        return stock_cached
