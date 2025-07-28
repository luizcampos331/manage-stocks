import re
from abc import ABC, abstractmethod
from typing import List, TypedDict

import httpx
from bs4 import BeautifulSoup


class StockPerformanceData(TypedDict):
    five_days: float
    one_month: float
    three_months: float
    year_to_date: float
    one_year: float


class StockCompetitors(TypedDict):
    name: str
    market_cap: object
    currency: str
    value: float


class GetStockWEbScrapingBySymbolOutput(TypedDict):
    company_name: str
    performance_data: StockPerformanceData
    competitors: List[StockCompetitors]


class StockWebScrapingGateway(ABC):
    @abstractmethod
    async def scraping_by_symbol(
        self, stock_symbol: str
    ) -> GetStockWEbScrapingBySymbolOutput:
        pass


class MarketWatchStockWebScrapingGateway(StockWebScrapingGateway):
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    PERFORMANCE_LABEL_MAP = {
        "5 Day": "five_days",
        "1 Month": "one_month",
        "3 Month": "three_months",
        "YTD": "year_to_date",
        "1 Year": "one_year",
    }

    def __init__(self):
        self.client = httpx.AsyncClient(
            headers=self.HEADERS, timeout=10, follow_redirects=True
        )

    def parse_marketcap_data(self, marketcap_str: str) -> dict:
        marketcap_str = marketcap_str.strip()
        match = re.match(r"([^\d\s]+)?([\d.,]+)([MBT])", marketcap_str.upper())

        if not match:
            return {"symbol": "UNKNOWN", "value": 0.0, "raw": marketcap_str}

        symbol, number_str, suffix = match.groups()
        number_str = number_str.replace(",", "")

        try:
            number = float(number_str)
        except ValueError:
            return {"symbol": "UNKNOWN", "value": 0.0, "raw": marketcap_str}

        factor = {"T": 1e12, "B": 1e9, "M": 1e6}.get(suffix, 1)
        value = number * factor

        return {
            "symbol": symbol.strip() if symbol else "UNKNOWN",
            "value": value,
        }

    async def scraping_by_symbol(
        self, symbol: str
    ) -> GetStockWEbScrapingBySymbolOutput:
        resp = await self.client.get(
            f"https://www.marketwatch.com/investing/stock/{symbol.lower()}"
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        company_name_tag = soup.find("h1", class_="company__name")
        company_name = (
            company_name_tag.get_text(strip=True)
            if company_name_tag
            else "Unknown Company"
        )

        performance = {}
        performance_table = soup.select_one("div.element--table.performance table")
        if performance_table:
            for row in performance_table.select("tr.table__row"):
                cols = row.find_all("td")
                if len(cols) >= 2:
                    label = cols[0].get_text(strip=True)
                    value_tag = cols[1].select_one("li.value.ignore-color")
                    if value_tag:
                        value_text = value_tag.get_text(strip=True).replace("%", "")
                        key = self.PERFORMANCE_LABEL_MAP.get(label)
                        if key:
                            try:
                                performance[key] = float(value_text)
                            except ValueError:
                                performance[key] = None

        competitors = []
        for row in soup.select("tbody.table__body tr.table__row"):
            cols = row.find_all("td")
            if len(cols) >= 3:
                name = cols[0].get_text(strip=True)
                marketcap_str = cols[2].get_text(strip=True)
                marketcap_info = self.parse_marketcap_data(marketcap_str)
                competitors.append(
                    {
                        "name": name,
                        "market_cap": {
                            "currency": marketcap_info["symbol"],
                            "value": marketcap_info["value"],
                        },
                    }
                )

        return {
            "company_name": company_name,
            "performance_data": performance,
            "competitors": competitors,
        }
