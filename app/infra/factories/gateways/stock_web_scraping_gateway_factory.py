import os

from app.infra.gateways.stock_web_scraping_gateway import (
    MarketWatchStockWebScrapingGateway,
)

implementations = {
    "market_watch": MarketWatchStockWebScrapingGateway,
}


class StockWebScrapingGatewayFactory:
    @staticmethod
    def make():
        implementation = os.getenv("STOCK_WEB_SCRAPING_IMPLEMENTATION")
        if implementation not in implementations:
            raise ValueError(
                f"Unsupported STOCK_WEB_SCRAPING_IMPLEMENTATION: {implementation}"
            )

        return implementations[implementation]()
